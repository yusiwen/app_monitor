import scrapy

from app_monitor.items import AppMonitorItem


class FilezillaSpider(scrapy.Spider):
    name = "filezilla"
    allowed_domains = ["filezilla-project.org"]
    start_urls = ["https://filezilla-project.org/download.php?show_all=1"]
    custom_settings = {"USER_AGENT": "app_monitor (+http://es.yusiwen.com)"}

    def parse(self, response, **kwargs):
        version = (
            response.xpath('//p[contains(text(), "latest stable version")]/text()')
            .get()
            .split(" ")[-1]
        )
        down_urls = [
            response.xpath('//a[contains(text(), "win64.zip")]/@href').get(),
            response.xpath('//a[contains(text(), "macos-x86.app")]/@href').get(),
            response.xpath('//a[contains(text(), "x86_64-linux-gnu.tar")]/@href').get(),
        ]

        item = AppMonitorItem()
        item["name"] = "FileZilla"
        item["version"] = version
        item["date"] = None
        item["notes"] = ""
        item["id"] = "filezilla"
        item["category"] = "tool"
        item["tags"] = ["ftp", "sftp"]
        item["project_url"] = "https://filezilla-project.org/"
        item["release_url"] = "https://filezilla-project.org/download.php?show_all=1"
        item["download_url"] = down_urls
        return item
