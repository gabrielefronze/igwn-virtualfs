from os import makedirs, path, mkdir, remove
from typing import List
import yaml
import subprocess

filePath = path.dirname(__file__)
basePath = path.join(filePath, "igwnfs")
framesConfigFileName = "framePaths.yml"


def linkPathByExp(base, exp, channel, period, name):
    return path.join(base, "exp", exp, channel, period, name)


def linkPathByPeriod(base, exp, channel, period, name):
    return path.join(base, "periods", period, exp, channel, name)


def ln(source, dest):
    bashCommand = f"ln -s {source} {dest}"
    print(f"{source} -> {dest}")
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def createLink(source, dest):
    if not path.exists(path.dirname(dest)):
        makedirs(path.dirname(dest))

    if path.exists(dest):
        remove(dest)

    ln(source, dest)


def initFrames():
    framesBasePath = path.join(basePath, "frames")

    if not path.isdir(basePath):
        mkdir(basePath)

    if not path.isdir(framesBasePath):
        mkdir(framesBasePath)

    with open(path.join(filePath, framesConfigFileName)) as framesConfigFile:
        config = yaml.load(framesConfigFile, Loader=yaml.FullLoader)
        for exp, channels in config.items():
            for channel in channels:
                for channelName, periods in channel.items():
                    for period in periods:
                        for periodName, links in period.items():
                            if links != "none":
                                if isinstance(links, List):
                                    for link in links:
                                        source, name = link.split(" -> ")
                                        dest = linkPathByExp(framesBasePath,
                                                             exp,
                                                             channelName,
                                                             periodName,
                                                             name)
                                        createLink(source, dest)
                                        dest = linkPathByPeriod(framesBasePath,
                                                                exp,
                                                                channelName,
                                                                periodName,
                                                                name)
                                        createLink(source, dest)
                                elif isinstance(links, str):
                                    source, name = links.split(" -> ")
                                    dest = linkPathByExp(framesBasePath,
                                                         exp,
                                                         channelName,
                                                         periodName,
                                                         name)
                                    createLink(source, dest)
                                    dest = linkPathByPeriod(framesBasePath,
                                                            exp,
                                                            channelName,
                                                            periodName,
                                                            name)
                                    createLink(source, dest)
    return


def init():
    if not path.exists(basePath):
        makedirs(basePath)

    initFrames()
    return


if __name__ == "__main__":
    init()
