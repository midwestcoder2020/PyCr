'''
Program Name: PCYR
Script Name: main.py
Version: 0.1
Python Version: 3.6
Author: midwestcoder
Github: https://github.com/midwestcoder2020
Website: www.midwestcoder.com
Date: 8 Sep 22

Purpose: The purpose of thins script is to provide a lighweight GUI platform for optical character recognition via pyton
the program allows for single and multiple file analysis for text witout the overhead of costs and hardware requirements of
third party software analysis and processing programs.
'''

from pathlib import Path
from gooey import Gooey
from gooey import GooeyParser
import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"/usr/local/bin/tesseract"
@Gooey(optional_cols=1, program_name="PyCR")
def main():
    desc = "Python Based Object Character Recognition!"
    parser = GooeyParser(description=desc, add_help=False)
    parser.add_argument('--verbose', help='be verbose', dest='verbose',
                        action='store_true', default=True)

    subs = parser.add_subparsers(help='commands',prog='NLTK Builder',dest='command')

    parser_one = subs.add_parser('pycr_single', prog="PyCR",help='Python Based Object Character Recognition!')
    parser_one.add_argument("--File-To-Search", default="", widget='FileChooser',help='Select the file to search')
    parser_one.add_argument('--Destination-Folder-Single',default='',widget='DirChooser',help='Select where to save the report')

    parser_two = subs.add_parser('pycr_multi', prog="Run OCR on entire collection", help='Detect OCR in a colletion of files')
    parser_two.add_argument('--Folder-To-Search',default='',widget='DirChooser',help='Select folder to perform OCR on')
    parser_two.add_argument('--Destination-Folder',default='',widget='DirChooser',help='Select where to save the report')

    args = parser.parse_args()

    if args.command == 'pycr_single':
        print("processing single file")
        print("Getting arguments")
        img= args.File_To_Search
        dest= args.Destination_Folder_Single

        print("checking file")
        checkImg(img,dest)


    elif args.command == 'pycr_multi':
        print("processing multiple files")
        print("Getting arguments")
        folder= args.Folder_To_Search
        dest= args.Destination_Folder
        p = Path(folder)
        imgList=[f for f in p.iterdir() if f.is_file()]
        for i in imgList:
            checkImg(i,dest)


def runOcr(img):
    try:
        text = pytesseract.image_to_string(img)
        return text
    except:
        return "n/a"

def checkImg(img,path):
    imgTextList = []
    text = runOcr(img)
    imgTextList.append({"path":os.path.basename(img),"text":text})
    reportImg(imgTextList,path)
    print("processing finished. Check results at "+os.path.join(path,'pycrdata.txt'))

def reportImg(dataList,path):
    print("writing results to file")
    with open(os.path.join(path,'pycrdata.txt'), 'a+', newline='') as file:
        for i in dataList:
            file.write("File Name >> : "+i['path']+"\n\n")
            file.write("File Text >> :")
            file.write("\n")
            file.write(i['text']+"\n")
            file.write("-"*20+"\n\n")

if __name__ == '__main__':
   main()