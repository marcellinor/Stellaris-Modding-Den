#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, io
from googletrans import Translator
import re


class LocList:
  def __init__(self, translateRest=False):
    self.languages=["braz_por","english","french","german","polish","russian","spanish"]
    self.languageCodes=["pt","en","fr", "de","pl","ru", "es"]
    # self.entries=[]
    self.entries=dict()
    self.dicts=dict()
    self.translateRest=translateRest
    for languageCode in self.languageCodes:
      self.dicts[languageCode]=dict()

  def addLoc(self, id, loc, language="en"):
    if language=="all":
      for k,d in self.dicts.items():
        d[id]=loc
    else:
      self.dicts[language][id]=loc
    return id
  def addEntry(self, gameLocId, string, complainOnOverwrite=False):
    if complainOnOverwrite:
      if gameLocId in self.entries:
        print("Warning: Overwriting loc entry!")
    self.entries[gameLocId]=string
    # self.entries.append([gameLocId, string])
    return gameLocId
  def append(self, gameLocId, string, complainOnOverwrite=False):
    return self.addEntry(gameLocId,string,complainOnOverwrite)
  def write(self,fileName, language, yml=True):
    if len(language)==2:
      languageCode=language
      language=self.languages[self.languageCodes.index(language)]
    else:
      languageCode=self.languageCodes[self.languages.index(language)]
    if self.translateRest:
      translator=Translator()

    localDict=self.dicts[languageCode]
    for englishKey, englishLoc in self.dicts["en"].items():
      # print(self.translateRest)
      if not englishKey in localDict:
        if self.translateRest:
          localDict[englishKey]=translator.translate(text=englishLoc, src="en", dest=languageCode).text
        else:
          localDict[englishKey]=englishLoc

    with io.open(fileName,'w', encoding="utf-8") as file:
      if yml:
        file.write(u'\ufeff')
        file.write("l_"+language+':\n')
      for key,entry in self.entries.items():
        if yml:
          file.write(" "+key+':0 "')
        awaitingVar=False
        for loc in re.split("(@| |\.|,|:|§|\)|\\n)",entry):
          if loc=="":
            continue
            # print("blub")
          if loc[0]=="@":
            awaitingVar=True
            # file.write(localDict[loc[1:]])
          elif awaitingVar:
            try:
              file.write(localDict[loc].replace("\n","\\n"))
              awaitingVar=False
            except:
              print(entry)
              print(loc)
              raise
          else:
            if loc=="\n":
              loc="\\n"
            file.write(loc)
        if yml:
          file.write('"')
        file.write("\n")

import shlex
import argparse
import glob

def parse(argv, returnParser=False):
  parser = argparse.ArgumentParser(description="")
  parser.add_argument('inputFileNames', nargs = '*' )
  parser.add_argument('--output_folder',default="test/localisation/" )
  parser.add_argument('--create_main_file', action="store_true")
  if returnParser:
    return parser
  parser.add_argument('--test_run', action="store_true", help="No Output.")
  
  
  args=parser.parse_args(argv)
  
  return(args)

def readYMLCreatePy(args,filePath="../cgm_buildings_script_source/localisation/english/cgm_building_l_english.yml"):
  fileName=os.path.basename(filePath)
  print(fileName)
  langCodeInFile=0
  locList=LocList()
  outArray=[]
  trivialAssignment=[]
  with io.open(filePath,'r', encoding="utf-8") as file:
    for line in file:
      lineArray=shlex.split(line)
      if not langCodeInFile and len(lineArray)!=0:
        for lang, langCode in zip(locList.languages, locList.languageCodes):
          if "l_"+lang in lineArray[0]:
            langCodeInFile=langCode
            languageInFile=lang
            break
        continue
      # print(line)
      outArray.append("")
      if ":" in line:
        key=lineArray[0].split(":")[0]
        outArray[-1]+='locList.addLoc("{}","{}","{}")'.format(key.replace(".","_"), lineArray[1],langCodeInFile)
        if args.create_main_file:
          trivialAssignment.append('locList.addEntry("{}","@{}")'.format(key,key.replace(".","_")))
        # contents.append(lineArray[1])
      for i,entry in enumerate(lineArray):
        if entry[0]=="#":
          outArray[-1]+=" ".join(lineArray[i:])
          break

  lastOutFile=""
  if not args.test_run:
    outFile=args.output_folder+"/locs/"+fileName.replace(".yml",".py")
    lastOutFile=outFile
    with open(outFile, "w") as file:
      # file.write("def locs(locList):\n")
      for entry in outArray:
        file.write(entry+"\n")
        # file.write("\t"+entry+"\n")
    if args.create_main_file:
      outFile=args.output_folder+"/"+fileName.replace(".yml","_main.py").replace("_l_"+languageInFile, "")
      lastOutFile=outFile
      with open(outFile, "w") as file:
        absPath=os.path.abspath(args.output_folder)
        commonPath=os.path.commonprefix([absPath, sys.path[0]])
        # print(commonPath)
        relPath=os.path.relpath(commonPath,absPath)
        # print(relPath)
        file.write("#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport os,sys,glob\n")
        file.write("os.chdir(os.path.dirname(__file__))\n")
        file.write("sys.path.insert(1, '"+relPath+"')\n")
        file.write("from locList import LocList\nlocList=LocList()\n")
        # file.write("import allModules,importlib\n")
        file.write("for fileName in glob.glob('locs/*.py'):\n")
        file.write("\twith open(fileName) as file:\n")
        file.write("\t\t exec(file.read())\n")
        # file.write("\t\t for line in file:\n")
        # file.write("\t\t\t try:\n")
        # file.write("\t\t\t\t eval(line)\n")
        # file.write("\t\t\t except:\n")
        # file.write("\t\t\t\t pass\n")

        # file.write('sys.path.insert(1, "test/locs/")\n')
        # file.write('packages=[]\n')
        # file.write('modules=[]\n')
        # file.write("allModules.load_all_modules_from_dir('test/locs/',modules,packages)\n")
        # file.write('for module,package in zip(modules,packages):\n')
        # file.write("\timportlib.import_module(module)\n")
        # file.write("\teval(package).locs(locList)\n")
        # for language in locList.languages:
        #   file.write("try:\n")
        #   file.write("\timport test_"+language+"\n")
        #   file.write("\ttest_"+language+".locs(locList)\n")
        #   file.write("except:\n")
        #   file.write("\tprint('No localisation given for {}')\n".format(language))
        # for entry in outArray:
        #   file.write(entry+"\n")
        for entry in trivialAssignment:
          file.write(entry+"\n")
        file.write('for language in locList.languages:\n'+
                    '\toutFolderLoc=language\n'+
                    '\tif not os.path.exists(outFolderLoc):\n'+
                      '\t\tos.makedirs(outFolderLoc)\n'+
                    '\tlocList.write(outFolderLoc+"/cgm_building_customize_l_"+language+".yml",language)')
  return lastOutFile


def main(args,*unused): #for gui compatibility

  if not os.path.exists(args.output_folder+"/locs"):
    os.makedirs(args.output_folder+"/locs")
    with open(args.output_folder+"/locs/__init__.py","w") as file:
      file.write(" ")
  globbedList=[]
  for b in args.inputFileNames:
    globbedList+=glob.glob(b)

  lastOutFile=""
  for inputFileName in globbedList:
    if inputFileName[-4:].lower()==".yml":
      lastOutFile=readYMLCreatePy(args, inputFileName)
  return lastOutFile

if __name__== "__main__":
  args=parse(sys.argv[1:])
  main(args)
  