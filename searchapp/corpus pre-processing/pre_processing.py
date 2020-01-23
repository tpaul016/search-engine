from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, ElementTree, SubElement
from pathlib import Path

with open("./UofO_Courses.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

Path('./corpus').mkdir(parents=True, exist_ok=True)
for tag in soup.find_all('div', class_= ['courseblock']):
    # parsing course
    split_text = tag.text.split('\n\n');
    course_title = split_text[0].replace('\n', '')
    split_title = course_title.split(' ')
    # checking if french course
    if int(split_title[1][1]) > 4 :
        continue
    course_code = split_title[0].lower() + split_title[1]
    course_desc = split_text[1] if len(split_text) > 1 else None

    # creating xml
    course = Element('course')
    title = SubElement(course, 'title')
    title.text = course_title
    desc = SubElement(course, 'desc')
    desc.text = course_desc
    tree = ElementTree(course)
    tree.write('./corpus/' + course_code + '.xml')
