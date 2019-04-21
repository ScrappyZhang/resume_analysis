# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import os
import json
from file2txt.read import read_doc, read_docx, read_txt, read_pdf


class Regulation_parsing_resume:
    '''
    基于规则解析简历
    '''
    def __init__(self):
        pass

    def print_one_resume_content(self, resume_fullname: str):
        '''
        输出一个简历的提取后的内容
        1) 以大类关键词下的子关键词为一个集合来输出
        2) 输出以该简历中的关键词的替代关键词输出，则为 content[1], 为默认
           输出以该简历中的关键词输出，则为 content[2], 即需把该函数中 content[1] 改为 content[2]
        :return: None
        '''
        # 注意！！！下面生成器必须要转化为列表或其他，否则需再次赋值（生成器的特性！！）
        a = list(self.Detail_again_parsing.parse_resume_content(self.Detail_again_parsing(), resume_fullname))
        a1 = [i for i in a if i[0] == '个人基本信息']
        a2 = [i for i in a if i[0] == '联系方式']
        a3 = [i for i in a if i[0] == '教育背景']
        a4 = [i for i in a if i[0] == '求职意向']
        a5 = [i for i in a if i[0] == '工作/实习经历与项目经验']
        a6 = [i for i in a if i[0] == '技能证书与荣誉']
        a7 = [i for i in a if i[0] == '自我评价']
        a8 = [i for i in a if i[0] == '校园经历']

        a1 = self.Detail_again_parsing.process_same_keyword_different_content(self.Detail_again_parsing(), a1)

        # print(*[a1, a2, a3, a4, a5, a6, a7, a8], sep='\n')

        a1_replace_key_list = list()
        a2_replace_key_list = list()
        for content in a1:
            a1_replace_key_list.append(content[1])
        for content in a2:
            a2_replace_key_list.append(content[1])

        reg_content = self.Detail_again_parsing.check_content(self.Detail_again_parsing(), resume_fullname)
        if reg_content:
            for content in reg_content:
                if content and content[0] == '个人基本信息' and content[1] not in a1_replace_key_list:
                    a1.append(content)
                if content and content[0] == '联系方式' and content[1] not in a2_replace_key_list:
                    a2.append(content)

        # TODO: 对 java工程师_1.txt , 教育背景的提取，因关键词与个人简介那里的关键词一模一样，而提取到个人简介那里了
        all_contents = [a1, a2, a3, a4, a5, a6, a7, a8]
        # for contents in all_contents:
        #     yield (contents)
        for contents in all_contents:
            content_temp = [i[3] for i in contents if i[3]]
            if content_temp:
                print('----------------------------------{total_key}----------------------------------'\
                      .format(total_key=contents[0][0]))
                for content in contents:
                    print(content[1], content[3].strip(), sep=' ----> ')
                print()
        return all_contents

    def content_dict(self, resume_fullname):
        d = dict()
        a = self.print_one_resume_content(resume_fullname)
        # a = list(contents_generator)
        for a1 in a:
            if a1:
                b = { i[2]:i[3] for i in a1 }
                d.update({a1[0][0]:b})
        # print(d)
        return d

    def print_more_resumes_content(self):
        '''
        1) 输出多个简历的提取后的内容
        2) 简历来源：./resume_txt 文件夹内的所有 txt 文件
        :return: None
        '''
        for root, dirs, files in os.walk('./resume'):
            file_list = [i for i in files if not i.startswith('~$')]

        for file in file_list:
            print('解析的简历为：{resume_name}'.format(resume_name=file))
            self.content_dict(file)
            print('==================================================='*3)

    class Roughly_parsing:
        def __init__(self):
            self.total_keywords = ['个人基本信息', '联系方式', '教育背景',
                                   '求职意向', '工作/实习经历与项目经验',
                                   '技能证书与荣誉', '自我评价', '校园经历']

        def dict_value_find_key(self, value: str) -> str:
            '''
            1) 该函数不需要调用了！！！
            2) 根据字典的值查询出对应的键
            3) 程序说明：
               resume_dict = {'经历': [{'校园经历': ['校园经历']}], '基本信息': [{'姓名': ['姓名', '名字']}, {'性别': ['性别']} ]}
               d = {'校园经历': ['校园经历'], '姓名啊': ['姓名', '名字'], '性别': ['性别']}
            4) 注意：对于 resume_dict 且 value = '微信',
                     ( main2_keyword_list.txt 中有多个 '其他', '微信' 不在最后那个 '其他' 中 ), 则该函数最后执行最后那个 return
            :param value: 值，eg: '名字'
            :return: 值对应的键，eg: '姓名'
            '''
            key_list = list()
            value_list = list()
            resume_dict = self.resume_total_keywords_str_to_dict()
            d = {list(j.keys())[0]: list(j.values())[0] for i in resume_dict.values() for j in i}

            for key, values in d.items():
                key_list.append(key)
                value_list.append(values)
            for index, values in enumerate(value_list):
                if value in values:
                    return key_list[index]
            return '其他'

        def resume_total_keywords_str_to_dict(self):
            '''
            1) 把 main2_keyword_list.txt 的内容转换成字典格式，部分如下所示：
              {
                '个人简介': [ {'姓名': ['姓名', '名字']}, {'性别': ['性别']}, {'民族': ['民族']} ],
                '校园经历': [ {'校园经历': ['校园经历']} ]
              }
            2) 注释部分: 把 dict --> str --> JSON 输出来，更直观，默认注释
            :return: dict   如上所示的字典
            '''

            with open('./main2_keyword_list.txt', 'rt', encoding='utf-8') as f:
                superset_keyword_dict = dict()
                superset_keyword_list = list()
                superset_keyword = ''

                lines = (line.strip() for line in f)
                for line in lines:
                    if line in self.total_keywords:
                        if superset_keyword_list:
                            superset_keyword_dict.update({superset_keyword: superset_keyword_list})
                            superset_keyword_list = []
                        superset_keyword = line
                        continue

                    '''
                    a = ''.split('：')
                    print(a)              # Output ['']
                    if a: print(1)        # Output 1
                    if a[0]: print(1)     # Output 
                    '''
                    subset_keyword = line.split('：')
                    if len(subset_keyword) >= 2:
                        subset_keyword_set = set(i for i in subset_keyword[1].split('、'))
                        subset_keyword_list = list(subset_keyword_set)
                        subset_keyword_dict = {subset_keyword[0]: subset_keyword_list}
                        superset_keyword_list.append(subset_keyword_dict)
                superset_keyword_dict.update({superset_keyword: superset_keyword_list})

            # superset_keyword_str = str(superset_keyword_dict).replace("'", '"')
            # superset_keyword_json = json.loads(superset_keyword_str)
            # print(json.dumps(superset_keyword_json, indent=2, ensure_ascii=False))

            superset_keyword_dict['个人基本信息'] = superset_keyword_dict.pop("")

            return superset_keyword_dict

        def change_resume_str(self, resume_fullname: str):
            '''
            1) 把某些简历中某些关键词中的空格符去掉，例如：“姓   名” -->  “姓名”
            2）去掉一些词，例如：“个人简介”，“个人资料”
            :param resume_fullname: 简历的全文件名，例如参数为：'Python 爬虫高级工程师.txt'
            :return: str   修改替换后的简历文本字符串
            '''
            if resume_fullname.endswith('.txt'):
                resume = read_txt('./resume/{}'.format(resume_fullname))
            elif resume_fullname.endswith('.doc'):
                try:
                    resume = read_doc('./resume/{}'.format(resume_fullname))
                except subprocess.CalledProcessError as e:
                    resume = ''
            elif resume_fullname.endswith('.docx'):
                resume = read_docx('./resume/{}'.format(resume_fullname))
            elif resume_fullname.endswith('.pdf'):
                resume = read_pdf('./resume/{}'.format(resume_fullname))
            else:
                resume = ''

            mytext = []
            text = re.split('\n+', resume)
            if re.match('第\s*\d\s*页', text[-1]):
                text.pop()
            for i in text:
                mytext.append(i)
            resume = '\n'.join(mytext)

            pattern = '←|_|✓|·|||●|||||◆|■|丨|\|'
            # pattern1 = '-'        # 2011-9 这种，还需考虑
            resume = re.sub(pattern, '', resume)

            resume = re.sub('姓\s{,9}名', '姓名', resume)
            resume = re.sub('性\s{,9}别', '性别', resume)
            resume = re.sub('籍\s{,9}贯', '籍贯', resume)
            resume = re.sub('学\s{,9}历', '学历', resume)
            resume = re.sub('身\s{,9}高', '身高', resume)
            resume = re.sub('专\s{,9}业', '专业', resume)
            resume = re.sub('手\s{,9}机', '手机', resume)
            resume = re.sub('手\s{,9}机\s{,9}号', '手机号', resume)
            resume = re.sub('民\s{,9}族', '民族', resume)
            resume = re.sub('电\s{,9}话', '电话', resume)
            resume = re.sub('邮\s{,9}箱', '邮箱', resume)
            resume = re.sub('邮\s{,9}编', '邮编', resume)
            resume = re.sub('住\s{,9}址', '住址', resume)
            resume = re.sub('年\s{,9}龄', '年龄', resume)
            resume = re.sub('基本信息|个人资料|个人信息', '', resume)
            resume = re.sub('\[pic\]', '', resume)

            return resume

        def parse_resume_total_keywords_dict(self):
            '''
            生成器，依次对应：eg: ('个人简介', '姓名', ['名字', '姓名'])
            :param resume_dict: 简历模板关键词文本(  main2_keyword_list.txt )转化成的字典结构
            :return: 生成器
            '''
            resume_dict = self.resume_total_keywords_str_to_dict()
            for i in resume_dict.items():
                for j in i[1]:
                    yield (i[0], list(j.keys())[0], list(j.values())[0])

        def parse_resume_keyword(self, resume_fullname: str):
            '''
            生成器，依次对应：
            ( main2_keyword_list.txt 中的总关键词, 该简历中的关键词的替代关键词, 该简历中的关键词,
              该简历中的关键词在该简历字符串中的位置(index), 该简历中的关键词的长度)
            eg: ('个人简介', '最高学历', '学历', 100, 2)
            :return: 生成器
            '''
            resume = self.change_resume_str(resume_fullname)
            all_keys = self.parse_resume_total_keywords_dict()
            for keys in all_keys:
                for key in keys[2]:
                    if re.finditer(key, resume):
                        for m in re.finditer(key, resume):
                            if not re.match('[\u4e00-\u9fa5()0-9a-zA-Z\/\\\]', resume[m.start() - 1]) and \
                                    not re.match('[\u4e00-\u9fa5()0-9a-zA-Z\/\\\]', resume[m.end()]):
                                yield (keys[0], keys[1], key, m.start(), len(key))

        def parse_resume_content(self, resume_fullname: str):
            '''
            生成器，依次生成：
            ( main2_keyword_list.txt 中的总关键词, 该简历中的关键词的替代关键词, 该简历中的关键词, 该简历中的关键词对应的资料项)
            eg: ('联系方式', '联系电话', '手机', '13XXXXXXXX94')
            :return: 生成器
            '''
            resume = self.change_resume_str(resume_fullname)
            keys_list = self.parse_resume_keyword(resume_fullname)
            keys_list = sorted(keys_list, key=lambda r: r[3])
            total_key_2, replace_key_2, resume_key_2, resume_key_index_2 = '', '', '', 0
            # print(keys_list)
            for num in range(len(keys_list) - 1):
                total_key_1, replace_key_1, resume_key_1, resume_key_index_1, resume_key_len_1 = keys_list[num]
                total_key_2, replace_key_2, resume_key_2, resume_key_index_2, resume_key_len_2 = keys_list[num + 1]
                content_index_left = resume_key_index_1 + resume_key_len_1 \
                    if resume[resume_key_index_1 + resume_key_len_1] != '：' \
                    else resume_key_index_1 + resume_key_len_1 + 1
                content_index_right = resume_key_index_2
                content = resume[content_index_left: content_index_right].strip()

                yield (total_key_1, replace_key_1, resume_key_1, content)
            yield (total_key_2, replace_key_2, resume_key_2, resume[resume_key_index_2:])

    class Detail_again_parsing(Roughly_parsing):
        def __init__(self):
            super().__init__()

        def find_emails_phone_age_and_work_experience(self, resume_fullname: str):
            '''
            正则匹配，返回 电子信箱 联系电话 岁数 工作年限
            :return: tuple
            '''
            resume = self.change_resume_str(resume_fullname)

            # TODO: 下面 phone 实际应用应该改一下，使得：比如不能匹配 139******** , 且位数必须为 11 位
            emails = re.findall(r'(\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*)', resume)
            phone = re.findall(r'1[\*\dxX]{8,10}[^()@\n]', resume)
            age = re.findall(r'\d{1,3}\s{0,5}岁', resume)

            work_experience = re.findall(r'\d{1,2}年[\u4e00-\u9fa5()]{,5}工作经验|'
                                         r'[一二三四五六七八九十零]{1,3}年[\u4e00-\u9fa5()]{,5}工作经验', resume)

            return emails, phone, age, work_experience
            # return emails[0][0], phone[0], age[0]

        def find_name_and_place(self, resume_fullname: str):
            '''
            以空格符或换行符分隔简历字符串，再返回其 姓名 和 居住地 ，都无则返回 None
            :param resume_fullname:
            :return:
            '''
            name, dwell_place =  '', ''
            resume = self.change_resume_str(resume_fullname)
            L = re.split('\s+|\n', resume)[:8]
            L = [i for i in L if 2 <= len(i) <= 4]
            # print(L)
            with open('./中国姓氏大全.txt', 'rt', encoding='utf-8') as f1:
                surnames = f1.read()
            with open('./中国地名大全.txt', 'rt', encoding='utf-8') as f2:
                toponymy = f2.read()
            for content in L:
                if content[0] in surnames and content not in toponymy \
                        and all([re.match('[\u4e00-\u9fa5]', i) for i in content]):
                    name = content
                    # print('姓名：', content)
                if content in toponymy and not content.isdigit():
                    dwell_place = content
                    # print('居住地：', content)

            return name, dwell_place

        def find_job(self, resume_fullname: str):
            pass

        def check_content(self, resume_fullname: str):
            '''
            1) 检查内容是否包含 电子信箱 or 联系电话 or 岁数 or 工作年限 or 姓名 or 居住地 的关键词，
            若都没包含则生成器为 None
            2) 生成器，依次为：
            eg: ('联系方式', '电子信箱', '邮箱', emails)
            :return: 生成器
            '''
            replace_key_list_1 = list()
            replace_key_list_2 = list()
            work_experience_result = ''
            contents = self.parse_resume_content(resume_fullname)
            for content in contents:
                if content[0] == '个人基本信息':
                    replace_key_list_1.append(content[1])
                    if content[1] == '工作年限':
                        work_experience_result = content[3]
                if content[0] == '联系方式':
                    replace_key_list_2.append(content[1])

            resume = self.change_resume_str(resume_fullname)
            emails, phone, age, work_experience = self.find_emails_phone_age_and_work_experience(resume_fullname)
            name, dwell_place = self.find_name_and_place(resume_fullname)
            emails = emails[0][0] if emails else None
            phone = phone[0] if phone else None
            age = age[0] if age else None
            work_experience = work_experience[0] if work_experience else None

            if '电子信箱' not in replace_key_list_2 and emails:
                yield ('联系方式', '电子信箱', '邮箱', emails)
            if '联系电话' not in replace_key_list_2 and phone:
                yield ('联系方式', '联系电话', '手机', phone)
            if '岁数' not in replace_key_list_1 and age:
                yield ('个人基本信息', '年龄', '岁数', age)
            if '工作年限' not in replace_key_list_1 and work_experience:
                yield ('个人基本信息', '工作年限', '工作年限', work_experience)
            if '姓名' not in replace_key_list_1 and name:
                yield ('个人基本信息', '姓名', '姓名', name)
            if '居住地' not in replace_key_list_1 and dwell_place:
                yield ('个人基本信息', '居住地', '居住地', dwell_place)
            yield None

        def process_content_colon(self, content: str):
            # TODO: 下面这块仅仅适用于 java工程师.docx 类的简历，此功能依后续情况 修改 或 删除(  复杂项，以后视情况单独细分 )
            '''
            切片出来的资料项，若包含有 '：' ，eg: a = '英语：\n良好\n听说：\n良好', 则输出如下：
            英语：良好
            听说：良好
            '''
            content2 = list()
            if '：' in content:
                b = re.split('\n', content)
                for i in range(len(b)):
                    if b[i].endswith('：') and len(b[i]) <= 2:   # 太不通用了，，暂留
                        if i + 1 <= len(b) - 1:
                            content2.append(''.join([b[i], b[i + 1]]))
            content2 = '\n'.join(content2)
            content = content2 if content2 else content

            return content

        def process_content_time_segment(self, total_key_1, content: str):
            # 匹配时间段 eg: 2013/7--2017/7
            pattern_time = '\d{4}/\d{1,2}[-~]{1,3}\d{4}/\d{1,2}|\d{4}.\d{1,2}[-~]{1,3}\d{4}.\d{1,2}|' \
                      '\d{4}/\d{1,2}至今|\d{4}.\d{1,2}至今|\d{4}[-~]{1,3}\d{1,2}至今|' \
                      '\d{4}年\d{1,2}月[-~至到]{1,3}\d{4}年\d{1,2}月'
            # 匹配数字序号 eg: ['一、', '三十五、', '3、']
            # pattern2 = '\d{1,2}[\.、]|[一二三四五六七八九十零]{1,3}[\.、]'

            content3 = list()
            if total_key_1 == '工作/实习经历与项目经验' \
                    or total_key_1 == '校园经历' \
                    or total_key_1 == '工作内容':
                a = re.finditer(pattern_time, content)
                if list(a):
                    content2 = [i.start() for i in a]
                    for num, i in enumerate(content2):
                        if len(content2) >= 2:
                            if num == 0:
                                content1 = content[0:content2[num + 1]]
                            elif num == len(content2) - 1:
                                content1 = content[i:]
                            else:
                                content1 = content[content2[num - 1]:i]
                            content3.append(content1)
            content4 = '\n'.join(content3)
            content = content4 if content4 else content

            return content

        def process_same_keyword_different_content(self, a: list):
            '''
            对一些关键词相同，但内容不大相同的内容，eg: 专业：	艺术设计 and 专业：	艺术设计	本科
            则保留资料项多的那一项
            :return:
            '''
            L = []
            for i in range(len(a)):
                for j in range(i + 1, len(a)):
                    if a[i][1] == a[j][1]:
                        L.append(a[i]) if len(a[i][3]) < len(a[j][3]) else L.append(a[j])
            for i in L:
                a.remove(i)
            return a

        def process_content_newline(self, content: str):
            '''
            1) 对于一些短的资料项，若有换行可合并为一行，美观
            2) 处理由读取文本而造成不合理的资料项换行
            :param content:
            :return:
            '''
            content4 = ''
            if len(content) < 30:
                content4 = re.sub('\n', '    ', content)
            content = content4 if content4 else content
            return content

        def process_content_start_with_keyword(self, content: str):
            content2 = ''
            for i in ['实习经历', '证书', '自我评价', '项目经验', '个人评价']:
                if content.startswith(i):
                    content2 = content[len(i):].lstrip()
                    break
            content = content2 if content2 else content
            return content

        def parse_resume_content(self, resume_fullname: str):
            '''
            # TODO: 应该不用重写的
           1) 处理提取的资料项 包含 '：' 的情况
           2) 处理 工作经历 等等，以时间段为分块显示
           3) 处理一些资料项 存在不好看的换行情况
           4) 处理一些解析出来的开头为关键词（重复）的资料项
           :return:
           '''
            resume_content_generator = super().parse_resume_content(resume_fullname)

            for contents in resume_content_generator:
                total_key_1, replace_key_1, resume_key_1, content = contents
                if content:
                    content = self.process_content_colon(content)
                    # content = self.process_content_time_segment(total_key_1, content)
                    content = self.process_content_newline(content)
                    content = self.process_content_start_with_keyword(content)
                    yield  total_key_1, replace_key_1, resume_key_1, content


if __name__ == '__main__':

    a = Regulation_parsing_resume()
    result = a.print_more_resumes_content()


