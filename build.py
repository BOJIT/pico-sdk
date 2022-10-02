# @file build.py
# @author James Bennion-Pedley
# @brief Checks the upstream pico-sdk for new tagged releases, then creates
#        a matching tagged commit if not present already.
# @date 27/09/2022
#
# @copyright Copyright (c) 2022


#----------------------------------- Imports ----------------------------------#

import git

#---------------------------------- Constants ---------------------------------#

SDK_URL = "https://github.com/raspberrypi/pico-sdk.git"
GIT_STR = "RUN git clone --depth 1 -b "
TARGET = "Dockerfile"

#----------------------------------- Helpers ----------------------------------#

def getRemoteTags(url):
    g = git.cmd.Git()
    blob = g.ls_remote(url, sort='-v:refname', tags=True, refs=True)
    entries = blob.split('\n')
    return list(map(lambda x: x.partition('refs/tags/')[2], entries))

def setDockerfileTag(tag):
    with open(TARGET, 'r', encoding='utf-8') as file:
        # Read file
        f = file.readlines()

        for idx, line in enumerate(f):
            idx_start = line.find(GIT_STR)
            idx_end = line.find(SDK_URL)

            # Replace tag line
            if (idx_start != -1) and (idx_end != -1):
                new_line = line[0:idx_start + len(GIT_STR)] + tag + line[idx_end - 1:]
                f[idx] = new_line

    # Write back file
    with open(TARGET, 'w') as file:
        file.writelines(f)

#--------------------------------- Entry Point --------------------------------#

# Pull pico-sdk tags
sdk_tags = getRemoteTags(SDK_URL)
repo = git.Repo('.')

# from oldest to newest release
for tag in sdk_tags[::-1]:
    # see if local tag exists
        if tag not in repo.tags:

            print(tag)

            # change pico-sdk tag
            setDockerfileTag(tag)

            # commit new dockerfile with tag
            repo.git.commit('-a', '-m', 'auto-build tag: ' + tag)
            repo.create_tag(tag, message=('auto-build tag: ' + tag))
            repo.git.push('--follow-tags')

