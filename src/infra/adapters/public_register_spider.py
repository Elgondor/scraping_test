import scrapy
import os
import json
from datetime import datetime

class PublicRegisterSpider(scrapy.Spider):
    name = 'public_register'
    start_urls = ['https://members.collegeofopticians.ca/Public-Register']
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 600,
        'CONCURRENT_REQUESTS': 1,
        'RETRY_TIMES': 10,
    }
    
    def __init__(self, *args, **kwargs):
        super(PublicRegisterSpider, self).__init__(*args, **kwargs)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.file_path = f'src/infra/data/scraped_data_{timestamp}.json'
    
    def parse(self, response):
        # Set page size to 50
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'ctl01$TemplateBody$WebPartManager1$gwpciNewQueryMenuCommon$ciNewQueryMenuCommon$ResultsGrid$Grid1$ctl00$ctl03$ctl01$PageSizeComboBox': '50'
            },
            callback=self.initiate_search
        )

    def initiate_search(self, response):
        # Click the "Find" button to initiate search
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'ctl00$MainContent$btnSearch': 'Find'},
            callback=self.parse_results
        )

    def parse_results(self, response):
        rows = response.css('.rgRow, .rgAltRow')
        scraped_data = []
        for row in rows:
            scraped_data.append({
                'registrant': row.css('td:nth-child(1)::text').get().strip() if row.css('td:nth-child(1)::text').get() else '',
                'status': row.css('td:nth-child(2)::text').get().strip() if row.css('td:nth-child(2)::text').get() else '',
                'class': row.css('td:nth-child(3)::text').get().strip() if row.css('td:nth-child(3)::text').get() else '',
                'practice_location': row.css('td:nth-child(4)::text').get().strip() if row.css('td:nth-child(4)::text').get() else '',
            })
        
        # Append data to file
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.extend(scraped_data)
        
        with open(self.file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
        
        next_page = response.css('input.rgPageNext::attr(name)').get()
        if next_page:
            formdata = {next_page: ' '}
            self.logger.info(f'Following to next page: {next_page}')
            yield scrapy.FormRequest.from_response(
                response,
                formdata=formdata,
                callback=self.parse_results
            )
        else:
            self.logger.info('No more pages')
