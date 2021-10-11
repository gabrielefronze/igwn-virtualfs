from os import makedirs, path, mkdir, removedirs, symlink, remove
import yaml
import subprocess

basePath = path.dirname(__file__)
framesConfigFileName = "framePaths.yml"


def getLinkPathByExp(base, exp, channel, period, name):
    return path.join(base, "exp", exp, channel, period, name)


def getLinkPathByPeriod(base, exp, channel, period, name):
    return path.join(base, "periods", period, exp, channel, name)\


def ln(source, dest):
    bashCommand = f"ln -s {source} {dest}"
    # print(bashCommand)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def initFrames():
    framesBasePath = path.join(basePath, "frames")

    if not path.isdir(framesBasePath):
        mkdir(framesBasePath)

    with open(path.join(basePath, framesConfigFileName)) as framesConfigFile:
        config = yaml.load(framesConfigFile, Loader=yaml.FullLoader)
        for exp, channels in config.items():
            # print(exp)
            # print(channels)
            for channel in channels:
                for channelName, periods in channel.items():
                    # print(channelName)
                    for period in periods:
                        for periodName, links in period.items():
                            # print(periodName)
                            # print(links)
                            if links != "none":
                                for link in links:
                                    # print(link)
                                    source, name = link.split(" -> ")
                                    dest = getLinkPathByExp(framesBasePath, exp, channelName, periodName, name)
                                    print(dest)
                                    makedirs(dest)
                                    ln(source, dest)
                                    dest = getLinkPathByPeriod(framesBasePath, exp, channelName, periodName, name)
                                    print(dest)
                                    makedirs(dest)
                                    ln(source, dest)
    return


def init():
    initFrames()
    return


if __name__ == "__main__":
    init()