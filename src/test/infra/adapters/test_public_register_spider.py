import os
import json
import pytest
import scrapy
from scrapy.http import HtmlResponse
from src.infra.adapters.public_register_spider import PublicRegisterSpider

@pytest.fixture
def spider():
    return PublicRegisterSpider()

@pytest.fixture(autouse=True)
def created_files():
    files = []
    yield files
    # This will run after each test
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)

def test_parse_results(spider, created_files):
    html_content = """
    <html>
    <body>
        <form id="test_form">
            <table>
                <tr class="rgRow">
                    <td>Registrant 1</td>
                    <td>Status 1</td>
                    <td>Class 1</td>
                    <td>Practice Location 1</td>
                </tr>
                <tr class="rgAltRow">
                    <td>Registrant 2</td>
                    <td>Status 2</td>
                    <td>Class 2</td>
                    <td>Practice Location 2</td>
                </tr>
            </table>
            <input class="rgPageNext" name="ctl00$MainContent$btnNextPage" />
        </form>
    </body>
    </html>
    """
    response = HtmlResponse(url='https://example.com', body=html_content, encoding='utf-8')
    results = list(spider.parse_results(response))

    # Track the file created by the spider
    created_files.append(spider.file_path)
    
    # Check the results
    assert len(results) == 1
    form_request = results[0]
    assert isinstance(form_request, scrapy.FormRequest)

    # Check the scraped data
    with open(spider.file_path, 'r') as f:
        scraped_data = json.load(f)
        assert len(scraped_data) == 2
        assert scraped_data[0]['registrant'] == 'Registrant 1'
        assert scraped_data[0]['status'] == 'Status 1'
        assert scraped_data[0]['class'] == 'Class 1'
        assert scraped_data[0]['practice_location'] == 'Practice Location 1'
        assert scraped_data[1]['registrant'] == 'Registrant 2'
        assert scraped_data[1]['status'] == 'Status 2'
        assert scraped_data[1]['class'] == 'Class 2'
        assert scraped_data[1]['practice_location'] == 'Practice Location 2'

@pytest.fixture(autouse=True)
def cleanup_files():
    created_files = []
    yield created_files
    # This will run after each test
    for file_path in created_files:
        if os.path.exists(file_path):
            os.remove(file_path)
