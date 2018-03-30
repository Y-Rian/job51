import requests
from parsel import Selector
import csv

url = 'https://www.51job.com/'
key = 'python爬虫'
# api = 'https://search.51job.com/list/040000,000000,0000,00,9,99,%s,2,1.html' % keyword  #040000 是城市的代码 python%25E7%2588%25AC%25E8%2599%25AB 是python爬虫
page = 10
area = '040000'   #深圳
job_info_list = []
def get_job_list(keyword,page_num,area):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36'
    }
    job_info = {}
    for i in range(1,2):

        search_api = 'https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html'.format(area,keyword,str(i))
        response = requests.get(search_api,headers=header)
        response.encoding = 'gbk'
        html = Selector(response.text)
        el_list = html.xpath('//div[@class="dw_table"]/div[@class="el"]')
        print(len(el_list))

        for el in el_list:
            # print(el.extract())
            job_name = el.xpath('.//p/span/a/@title')[0].extract()
            job_url = el.xpath('.//p/span/a/@href')[0].extract()
            company = el.xpath('.//span[@class="t2"]/a/@title')[0].extract()
            job_addr = el.xpath('.//span[@class="t3"]/text()')[0].extract()
            salary = el.xpath('.//span[@class="t4"]/text()')[0].extract()
            publish_date = el.xpath('.//span[@class="t5"]/text()')[0].extract()
            job_info = {
                'job_name': job_name,
                'company': company,
                'job_addr': job_addr,
                'salary': salary,
                'publish_date': publish_date,
                'job_url': job_url
            }
            job_info_list.append(job_info)
        return job_info_list

def write2csv(list):
    csv_headers = ['job_name','company',  'job_addr', 'salary', 'publish_date','job_url']
    with open('jobs.csv','w',newline='') as f:
        f_csv = csv.DictWriter(f, csv_headers)
        f_csv.writeheader()
        f_csv.writerows(job_info_list)
        print('写入完成')


def main():
    # key = '爬虫工程师'
    key = 'python爬虫'
    page = 10
    area = '040000'
    job_list = get_job_list(key,page,area)
    write2csv(job_list)

if __name__=='__main__':
    main()