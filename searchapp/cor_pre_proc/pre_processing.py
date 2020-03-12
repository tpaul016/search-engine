from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, ElementTree, SubElement
from pathlib import Path
import os

# if the reuters corpus will be created
process_reuters = False

def createCourseCorpus(path):
    currDir = os.getcwd()
    os.chdir(path)

    with open("./UofO_Courses.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    Path('./corpus').mkdir(parents=True, exist_ok=True)
    for tag in soup.find_all('div', class_= ['courseblock']):
        # parsing course
        split_text = tag.text.split('\n\n');
        course_title = split_text[0].replace('\n', '')
        split_title = course_title.split(' ')
        # checking if french course
        if int(split_title[1][1]) > 4:
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

    os.chdir(currDir)


def create_reuters_corpus(dir_path):
    article_id = 0
    Path('./reuters/processed').mkdir(parents=True, exist_ok=True)
    file_paths = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]

    for path in file_paths:
        if not path.endswith(".sgm"):
            continue

        with open(path) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        for tag in soup.find_all('reuters'):
            # parsing reuters
            date_text = tag.find('date').text
            topics_text = ','.join(list(map(lambda x: x.text, tag.find('topics').contents)))
            try:
                title_text = tag.find('title').text
            except:
                title_text = title.text
            try:
                body_text = tag.find('body').text
            except:
                body_text = body.text

            # creating xml
            reuters = Element('reuters')
            date = SubElement(reuters, 'date')
            date.text = date_text
            topics = SubElement(reuters, 'topics')
            topics.text = topics_text
            title = SubElement(reuters, 'title')
            title.text = title_text
            body = SubElement(reuters, 'body')
            body.text = body_text
            tree = ElementTree(reuters)
            tree.write('./reuters/processed/reuters-' + str(article_id) + '.xml')
            article_id += 1

if process_reuters:
    create_reuters_corpus('./reuters/raw')

# If running file as main program
if __name__ == "__main__":
    createCourseCorpus(os.getcwd())
