[TOC]

# 1.  工程目录

```D
./
│  main.py
│  main_keyword_list.txt
|  README.md
│  中国地名大全.txt
│  中国姓氏大全.txt
│
├─file2txt
│  │  read.py
│  │  __init__.py
│
├─resume
```



# 2.  main_keyword_list.txt 结构示例说明

```D
求职意向

目标行业：目标行业、目标领域、希望行业、意向行业、工作意向
目标职位：目标职位、期望职位、目标岗位、期望职位、期望岗位、求职意向、应聘职位、从事职业、目标职能、意向职位、应聘岗位
工作性质：工作性质
期望薪资：期望薪资、薪金要求、目标薪酬、期望月薪、期望年薪、薪资要求
期望工作地：期望工作地区、期望工作地点、目标工作地区、目标工作地点、目标地点、意向城市、意向工作地
何时到岗：何时到岗、到岗时间
其他：福利待遇、上班时间、假期待遇、五险一金
```

> 总关键词：上面示例中的 `求职意向` ，仅一个
>
> 大关键词：上面示例中的 `目标行业` ， `目标职位` 等等，有多个
>
> 小关键词：上面示例中的 `目标行业` ， `目标领域` 等等，有多个



# 3.  /file2txt/read.py 文件

<u>自定义模块，功能为把不同格式的简历文件读取成文本，目前支持读取的简历文件格式为 `doc、docx、pdf，txt`</u>



# 4.  /main.py 文件

**总体思路**：

1. 处理简历读取的文本，去除特殊符号，无关词，等等

2. 把 `main_keyword_list.txt`文件的内容转成<u>字典格式</u>，如下所示（有删减，仅作说明）：

```python
{
       '个人简介': [ {'姓名': ['姓名', '名字']}, {'性别': ['性别']}, {'民族': ['民族']} ],
       '校园经历': [ {'校园经历': ['校园经历']} ]
}
```

3. 依每个大关键词返回生成器，例如：`('个人简介', '姓名', ['名字', '姓名'])`  等等

4. 通过遍历的方法，得到简历中的小关键词在该简历字符串中的位置（index）, 以及该简历中的小关键词的长度，依此进一步处理上面返回的生成器为 `('个人简介', '姓名', '姓名', 10, 2)`

5. 由上面生成器的相邻的两个小关键词的位置和长度，截取得到这两个小关键词中的第一个小关键词对应的资料项，再依此进一步处理上面返回的生成器为 `('个人简介', '姓名', '姓名', '小白')`

---
> 判断若没有 `电子信箱，联系电话，岁数，姓名，地名` 这些关键词，则进行以下操作找出相应的资料项
>
> 再处理成跟第 5 步格式相符合的生成器，，

6. 对于缺少关键词的部分资料项，通过正则匹配的方法，匹配出 `电子信箱，联系电话，岁数` 这些资料项
7. 对于缺少关键词的 `姓名，地名`这些资料项，结合 `中国地名大全.txt` 和 `中国姓氏大全.txt`以及 `姓名，地名`这些资料项的特点来匹配出这些资料项

至此，简历中的关键词（须`main_keyword_list.txt`存在的）以及其相对应的资料项都已一一提取出来。。



# 5.  待完善

略...
