import os

import openpyxl

from utils import crawl_post


def convert_to_xlsx():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['제목', '주소'])
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 40

    with open('data/result.csv', 'r') as f:
        for line in f.readlines():
            title = line.split('\t')[0]
            href = line.split('\t')[1]
            ws.append([title, href])

    wb.save('data/result.xlsx')

def main():
    # csv에서 값만 읽고 페이지 당 content 긁어오기

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['제목', '내용'])

    csv_path = os.path.join('data', 'result.csv')
    with open(csv_path) as f:
        post_list = f.readlines()
        for post in post_list:
            title = post.split('\t')[0]
            href = post.split('\t')[1]
            content = crawl_post(href)

            ws.append([title, content])

    wb.save(os.path.join('data', 'post_result.xlsx'))


if __name__ == '__main__':
    main()