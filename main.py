import random
import downloadlink as D
import time
'''
自己写的一个关于壁纸的爬虫，
翻了翻网页感觉 https://wall.alphacoders.com/ 这个网站的图片质量很好。
批量下载一下，顺便练练手
模块会一点点完善
'''

if __name__ == "__main__":
    main_html,link = D.search_mainpage()
    #max_num = D.max_num(main_html)
    i = input("你希望下载多少页图片？（1页有30个图片）：")
    count = 1
    j = input("你想从第几页下载？：")
    count = int(j)
    while(count <= int(i)):
        print("--------------------page"+str(count))
        main_html = D.change_mainpage(link,count)
        id,service_tag,info = D.link_dialog(main_html)
        pic_num = 0
        while(pic_num < len(id)):
            print("   |------------"+str(pic_num + 1)+r'---'+id[pic_num])
            pic_url = D.merge_url(id,pic_num)
            D.download_pic(pic_url,id[pic_num],service_tag[pic_num])
            pic_num += 1
            time.sleep(random.randint(1,2))
        count += 1
        print("休息一下-------：）））））））别被封号了。")
        time.sleep(random.randint(5, 9))
