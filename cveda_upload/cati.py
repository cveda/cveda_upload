# -*- coding: utf-8 -*-

# Copyright (c) 2016 CEA
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from datetime import datetime
import os

LOGGER = None
CATI_WORFLOW_DIRECTORY = None
SENT_FILE = 'sent.csv'
RESPONSE_FILE = 'response.csv'
DONE_FILE = 'done.csv'
LINE_SEP = '\n'
COL_SEP = ';'


##############################################################################
def is_system_OK():
    """ Return True if all needs files are readable and writable, otherwise
        log the missing permissions and return False.
    """

    # check root directory
    if not os.path.exists(CATI_WORFLOW_DIRECTORY):
        os.makedirs(CATI_WORFLOW_DIRECTORY)
    # check sent, response and done files (exists, readable, writable)
    paths = [
        get_sent_file_path(),
        get_response_file_path(),
        get_done_file_path()
    ]
    message = ''
    for path in paths:
        if not os.access(path, os.F_OK):
            open(path, 'a').close()
        if not os.access(path, os.R_OK):
            message += "{} has not read access.\n".format(path)
        if not os.access(path, os.W_OK):
            message += "{} has not write access.\n".format(path)

    # log and return
    if message != '':
        LOGGER.critical(message)
        return False
    else:
        return True


##############################################################################
def get_sent_file_path():
    """ Build and return the file path containing the list of sent files """

    return "{0}/{1}".format(CATI_WORFLOW_DIRECTORY, SENT_FILE)


##############################################################################
def get_response_file_path():
    """ Build and return the file path containing the list of cati responses.
    """

    return "{0}/{1}".format(CATI_WORFLOW_DIRECTORY, RESPONSE_FILE)


##############################################################################
def get_done_file_path():
    """ Build and return the file path containing
        the list of done files (sent and response).
    """

    return "{0}/{1}".format(CATI_WORFLOW_DIRECTORY, DONE_FILE)


##############################################################################
def read_sent_file():
    """ Read the file containing the list of sent files and return
        a dictionnary with :
        - sent file name as key
        - sent time as value
        The row file format is 2 values separated by the COL_SEP value
        and endding by the LINE_SEP value.
    """

    sent = {}
    lines = [line.rstrip(LINE_SEP) for line in open(get_sent_file_path())]
    for line in lines:
        split = line.split(COL_SEP)
        sent[split[0]] = split[1]
    return sent


##############################################################################
def read_response_file():
    """ Read the file containing the list of cati responses return
        a dictionnary with :
        - sent file name as key
        - status and optionnal rejected message as value.
        The status values must be 'Rejected' or 'Validated'.
        The row file format is 2 or 3 values separated by the COL_SEP value
        and endding by the LINE_SEP value.
    """
    responses = {}

    lines = [line.rstrip(LINE_SEP) for line in open(get_response_file_path())]
    for line in lines:
        split = line.split(COL_SEP, 1)
        responses[split[0]] = split[1]
    return responses


##############################################################################
def has_sent(entry):
    """ Return True if entry sent, False otherwize.

    Pameters:
        entry: Representing the file name
    """

    sent = read_sent_file()
    return entry in sent.keys()


##############################################################################
def get_response(entry):
    """ Return a list containing status and optionnal rejected message,
        None otherwise.,

    Pameters:
        entry: Representing the file name
    """
    responses = read_response_file()
    if entry not in responses.keys():
        return None
    else:
        return responses[entry].split(COL_SEP)


##############################################################################
def add_sent(entry):
    """ Add an entry and time
        in the file containing the list of sent entries

    Pameters:
        entry: Representing the file name
    """
    if not has_sent(entry):
        with open(get_sent_file_path(), 'a') as sentfile:
            sentfile.write("{0}{1}{2}{3}".format(
                entry, COL_SEP, datetime.now(), LINE_SEP)
            )


##############################################################################
def send_file_by_sftp(filepath, fields):
    print 'cati.send_file_by_sftp NOT IMPLEMENTED'


##############################################################################
def send_entry(entry, filepath, fields):
    """ Send the file reprensenting by filepath to cati repository

    Pameters:
        entry: Representing the file name
        filepath: the file to send (path and file name generated by cubicweb)
        fields: dictionnary of upload fields
    """

    if not has_sent(entry):
        try:
            send_file_by_sftp(filepath, fields)
            add_sent(entry)
            LOGGER.info("{} sent to cati".format(entry))
        except BaseException as e:
            LOGGER.critical("{} not sent to cati cause {}".format(entry, e))


##############################################################################
def set_done(entry):
    """ Add to the done entries file the entry with sent time and response.
        Remove also entry in sent and response files

    Pameters:
        entry: Representing the file name
    """

    sent = read_sent_file()
    responses = read_response_file()
    if entry in sent.keys() and entry in responses.keys():
        with open(get_done_file_path(), 'a') as entryfile:
            entryfile.write("{0}{1}{2}{3}{4}{5}{6}{7}".format(
                datetime.now(), COL_SEP,
                entry, COL_SEP,
                sent[entry], COL_SEP,
                responses[entry], LINE_SEP)
            )
        value = sent.pop(entry)
        with open(get_sent_file_path(), 'w') as entryfile:
            for value in sent.values():
                entryfile.write("{0}{1}{2}{3}".format(
                    entry, COL_SEP, value, LINE_SEP)
                )
        value = responses.pop(entry)
        with open(get_response_file_path(), 'w') as entryfile:
            for value in sent.values():
                entryfile.write("{0}{1}{2}{3}".format(
                    entry, COL_SEP, value, LINE_SEP)
                )
