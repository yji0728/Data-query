"""
Web Data Extractor
Extracts data from web pages using BeautifulSoup and requests.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import logging
import time


class WebExtractor:
    """Extracts data from web sources."""
    
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        """
        Initialize web extractor.
        
        Args:
            headers: Optional HTTP headers to use for requests
        """
        self.logger = logging.getLogger(__name__)
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def fetch_url(self, url: str, timeout: int = 30) -> Optional[str]:
        """
        Fetch HTML content from a URL.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            HTML content as string, or None if request fails
        """
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            self.logger.info(f"Successfully fetched: {url}")
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching URL {url}: {e}")
            return None
            
    def parse_html(self, html: str, parser: str = "lxml") -> Optional[BeautifulSoup]:
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html: HTML content as string
            parser: Parser to use (lxml, html.parser, etc.)
            
        Returns:
            BeautifulSoup object
        """
        try:
            soup = BeautifulSoup(html, parser)
            return soup
        except Exception as e:
            self.logger.error(f"Error parsing HTML: {e}")
            return None
            
    def extract_table(self, url: str, table_selector: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Extract table data from a web page.
        
        Args:
            url: URL of the web page
            table_selector: CSS selector for the table (optional)
            
        Returns:
            List of dictionaries containing table data
        """
        html = self.fetch_url(url)
        if not html:
            return []
            
        soup = self.parse_html(html)
        if not soup:
            return []
            
        # Find table
        if table_selector:
            table = soup.select_one(table_selector)
        else:
            table = soup.find('table')
            
        if not table:
            self.logger.warning("No table found on page")
            return []
            
        # Extract headers
        headers = []
        header_row = table.find('thead')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
        else:
            # Try to find headers in first row
            first_row = table.find('tr')
            if first_row:
                headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])]
                
        if not headers:
            self.logger.warning("No headers found in table")
            return []
            
        # Extract data rows
        data = []
        tbody = table.find('tbody') or table
        rows = tbody.find_all('tr')[1 if not table.find('thead') else 0:]
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) == len(headers):
                row_data = {headers[i]: cells[i].get_text(strip=True) 
                           for i in range(len(headers))}
                data.append(row_data)
                
        self.logger.info(f"Extracted {len(data)} rows from table")
        return data
        
    def extract_elements(self, url: str, selector: str, 
                        attributes: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Extract elements from a web page using CSS selector.
        
        Args:
            url: URL of the web page
            selector: CSS selector for elements
            attributes: List of attributes to extract from each element
            
        Returns:
            List of dictionaries containing element data
        """
        html = self.fetch_url(url)
        if not html:
            return []
            
        soup = self.parse_html(html)
        if not soup:
            return []
            
        elements = soup.select(selector)
        data = []
        
        for idx, element in enumerate(elements):
            item = {
                'text': element.get_text(strip=True),
                'html': str(element)
            }
            
            if attributes:
                for attr in attributes:
                    item[attr] = element.get(attr, '')
                    
            data.append(item)
            
        self.logger.info(f"Extracted {len(data)} elements")
        return data
        
    def extract_links(self, url: str, filter_pattern: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Extract links from a web page.
        
        Args:
            url: URL of the web page
            filter_pattern: Optional pattern to filter links
            
        Returns:
            List of dictionaries containing link data
        """
        html = self.fetch_url(url)
        if not html:
            return []
            
        soup = self.parse_html(html)
        if not soup:
            return []
            
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            
            if filter_pattern and filter_pattern not in href:
                continue
                
            links.append({
                'url': href,
                'text': text,
                'title': link.get('title', '')
            })
            
        self.logger.info(f"Extracted {len(links)} links")
        return links
        
    def extract_custom(self, url: str, extraction_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data using custom configuration.
        
        Args:
            url: URL of the web page
            extraction_config: Dictionary containing extraction rules
            
        Returns:
            Dictionary containing extracted data
        """
        html = self.fetch_url(url)
        if not html:
            return {}
            
        soup = self.parse_html(html)
        if not soup:
            return {}
            
        result = {}
        
        for field_name, config in extraction_config.items():
            selector = config.get('selector')
            attr = config.get('attribute')
            multiple = config.get('multiple', False)
            
            if multiple:
                elements = soup.select(selector)
                if attr:
                    result[field_name] = [el.get(attr, '') for el in elements]
                else:
                    result[field_name] = [el.get_text(strip=True) for el in elements]
            else:
                element = soup.select_one(selector)
                if element:
                    if attr:
                        result[field_name] = element.get(attr, '')
                    else:
                        result[field_name] = element.get_text(strip=True)
                else:
                    result[field_name] = None
                    
        self.logger.info(f"Extracted custom data with {len(result)} fields")
        return result
