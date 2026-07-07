import os
import argparse
from pathlib import Path

ARGUMENTS={}

def args_init():
    if not ARGUMENTS:
        ARGUMENTS["BASEDIR"] = Path(__file__).resolve().parent.parent
        parser = argparse.ArgumentParser()
        parser.add_argument("-b", "--basedir", "--base", dest="basedir")
        parser.add_argument("-c", "--config", "--configpath", dest="configpath")
        args = parser.parse_args()
        if args.basedir is not None:
            basedir= Path(args.basedir)
            if basedir.is_dir():
                ARGUMENTS["BASEDIR"] = basedir
        
        if args.configpath is not None:
            configpath= Path(args.configpath)
            if configpath.is_file():
                ARGUMENTS["CONFIGPATH"] = configpath

        if "CONFIGPATH" not in ARGUMENTS:
            configpath = ARGUMENTS["BASEDIR"] / "data/config.json"
            ARGUMENTS["CONFIGPATH"] = configpath

def args_get_basedir():
    args_init()
    return ARGUMENTS["BASEDIR"]

def args_get_configpath():
    args_init()
    return ARGUMENTS["CONFIGPATH"]

