#!/Users/lalitaalaalitah/.pyenv/versions/3.8.13/envs/id/bin/python
#
#
# v1    :   delete useless PDF and keep a record.
#
# v2 : 20221024 :   show size of total deleted files and total kept files. Also, initially run check for all undesired PDF which are downloaded again by another script, then delete them all.
#
#
# v3 :  20230121    :   added a way to kill skim after confirmation.
import os
import math
import sys
import subprocess
# import argparse
import pickle
import time
#
#
#
sys.path.append("/Users/lalitaalaalitah/MyScripts")
from move_to_similar_folder import (
    create_same_folder_structure,
    move_file_to_similar_path,
)


ROOT_DIR = "/Volumes/14TB_EXOS_28102020/archive.org"
DATA_ROOT_DIR = "/Volumes/14TB_EXOS_28102020/UserDataForMac/Documents/Github/archive_downloader/07_DeleteUselssPDF"

# open helper file
os.system(
    "code /Volumes/14TB_EXOS_28102020/UserDataForMac/Documents/Github/PanditMagazine/folder_path_to_link.md"
)


def create_list_of_available_pdf_paths(
    root_dir_1,
    available_file_paths_pickle_path_2,
):
    """create list of paths of pdf in archive dir"""
    list_of_available_pdf_paths_1 = []
    # create a list of pdf paths
    for root, dirs, files in os.walk(root_dir_1):
        for each_file in files:
            each_file_path = os.path.join(root, each_file)
            if (
                each_file.endswith(".pdf")
                and each_file_path not in list_of_available_pdf_paths_1
            ):
                list_of_available_pdf_paths_1.append(each_file_path)
    # pickle dump
    with open(available_file_paths_pickle_path_2, "wb") as poloapp2:
        pickle.dump(list_of_available_pdf_paths_1, poloapp2)
    #
    return list_of_available_pdf_paths_1


def make_a_list_of_non_tracked_missing_pdf(
    list_of_available_pdf_paths_old_1,
    list_of_missing_pdf_paths_old_1,
    missing_file_paths_pickle_path_1,
    trash_dir,
    list_of_deleted_pdf_paths_3,
):
    """AI is creating summary for make_a_list_of_non_tracked_missing_pdf

    Args:
        list_of_available_pdf_paths_old_1 ([list]): [old list of all pdf paths which were available at last run.]
        list_of_missing_pdf_paths_old_1 ([list]): [list of those pdf which were not recorded while deleting, either by this script of manually.]
        missing_file_paths_pickle_path_1 ([file_path]): [path of pickle file to store list_of_missing_pdf_paths_old_1]
    """
    # Now remove non existent pdf paths from the list of missing pdf, if they are either present in Trash dir or are present in archive dir. If they are not present in Trash dir, then add to list of missing pdf paths.
    # iterate over old list of available pdf pdths.
    for each_pdf_path_1 in list_of_available_pdf_paths_old_1:
        # generate path for each_pdf if it was moved in Trash dir.
        each_pdf_path_1_in_trash = each_pdf_path_1.replace(ROOT_DIR, trash_dir)
        # print(f'{each_pdf_path_1} exits : {os.path.isfile(each_pdf_path_1)}')
        # print(f'{each_pdf_path_1_in_trash} exists : {os.path.isfile(each_pdf_path_1_in_trash)}')
        # if pdf doesn't exist now, then.
        if not os.path.isfile(each_pdf_path_1):
            # if pdf is not present in trash dir too, then add to list of missing paths.
            if not os.path.isfile(each_pdf_path_1_in_trash):
                list_of_missing_pdf_paths_old_1.append(each_pdf_path_1)
            # if pdf is present in trash dir, then remove it from list of missing pdf paths.
            else:
                if each_pdf_path_1 in list_of_missing_pdf_paths_old_1:
                    list_of_missing_pdf_paths_old_1.remove(each_pdf_path_1)
        # if pdf is present in the archive dir, then.
        else:
            # if pdf is present in list_of_missing_pdf_paths, then remove it from the list.
            if each_pdf_path_1 in list_of_missing_pdf_paths_old_1:
                list_of_missing_pdf_paths_old_1.remove(each_pdf_path_1)
    # 
    # Remove pdf path from list of missing pdf paths, if the pdf path is present in list of deleted pdf paths.
    # Now iterate over the list of missing PDF paths which is corrected by matching to Trash path and old list of available pdf paths.
    for each_pdf_path_2 in list_of_missing_pdf_paths_old_1:
        # if pdf path is present in list of deleted PDF paths, then remove it from list of missing PDF paths.
        if each_pdf_path_2 in list_of_deleted_pdf_paths_3:
            list_of_missing_pdf_paths_old_1.remove(each_pdf_path_2)

    #
    # pickle dump
    with open(missing_file_paths_pickle_path_1, "wb") as mfppp1:
        pickle.dump(list_of_missing_pdf_paths_old_1, mfppp1)
    #
    return list_of_missing_pdf_paths_old_1


def delete_pdf(
    pdf_path,
    list_of_deleted_pdf_paths_2,
    delete_confirmation_1,
    list_of_desired_pdf_paths_old_1,
    trash_dir,
    list_of_deleted_pdf_paths,
    size_of_delete_pdf_2
):
    """AI is creating summary for delete_pdf

    Args:
        pdf_path ([type]): [description]
        list_of_deleted_pdf_paths_2 ([type]): [description]
    """
    print(f"handing {pdf_path}")
    # get file size of this pdf in bytes and MB and truncated digits.
    # get pdf file size in bytes.
    pdf_file_size_raw = os.path.getsize(pdf_path)
    # convert size from bytes to MB
    pdf_file_size_MB = pdf_file_size_raw / (1024 * 1024)
    # truncate to 3 digits after decimal
    pdf_file_size = math.trunc(10**3 * pdf_file_size_MB) / 10**3
    print(f"size of this pdf is {pdf_file_size} MB.")
    # delete pdf
    # confirm that pdf still exists.
    if os.path.isfile(pdf_path):
        # if pdf is present in older list of deleted pdf paths, delete it again and warn to correct downloader scripts.
        if pdf_path in list_of_deleted_pdf_paths:
            print(
                f"{pdf_path}\t was already mentioned as undesired, so we are deleting it again. Check your download script which is downloading it again and again!!"
            )
            os.remove(pdf_path)
            if not os.path.isfile(pdf_path):
                print("deleted it correctly.")
                print(f'we freed {pdf_file_size} MB of space.')
        else:
            if "'" in pdf_path:
                os.system(f'open "{pdf_path}"')
            else:
                os.system(f"open '{pdf_path}'")
            keep_or_not = input("do you want to delete this pdf ? Yes(y), No(any key)")
            # # close skim
            subprocess.call("killall Skim", shell=True)
            #
            if keep_or_not in ["y", "य"]:
                if delete_confirmation_1 == "d":
                    try:
                        print(f"deleting {pdf_path} now")
                        os.remove(pdf_path)
                        # add pdf to a list.
                        if not os.path.isfile(pdf_path):
                            list_of_deleted_pdf_paths_2.append(pdf_path)
                        #
                        print(f"deleted the pdf {pdf_path}")
                        print(f'we freed {pdf_file_size} MB of space.')
                        size_of_delete_pdf_2 += pdf_file_size
                        print(f'Total size of deleted pdf-s in this session is :{size_of_delete_pdf_2}')
                    except Exception as exception_x:
                        print(exception_x)
                        print("failed to delete the pdf.")
                else:
                    pdf_path_in_trash_dir = pdf_path.replace(ROOT_DIR, trash_dir)
                    # # create similar path if needed
                    # create_same_folder_structure(ROOT_DIR, trash_dir)
                    try:
                        print(
                            f"moving the\n\t{pdf_path}\nto\n\t{pdf_path_in_trash_dir}"
                        )
                        # os.rename(pdf_path, pdf_path_in_trash_dir)
                        pdf_file_root, pdf_file_name = os.path.split(pdf_path)
                        # print(f'move_file_to_similar_path("{pdf_file_name}", "{pdf_file_root}", "{ROOT_DIR}", "{trash_dir}", "a")')
                        move_file_to_similar_path(
                            pdf_file_name, pdf_file_root, ROOT_DIR, trash_dir, "a"
                        )
                        # add pdf to a list.
                        if not os.path.isfile(pdf_path):
                            list_of_deleted_pdf_paths_2.append(pdf_path)
                            #
                            print(
                                "moved"
                            )  # the\n\t{pdf_path} to\n\t{pdf_path_in_trash_dir}")
                        else:
                            print("failed to move.")
                    except Exception as exception_x:
                        print(exception_x)
                        print(f"failed to move the pdf to {trash_dir}.")
            else:
                list_of_desired_pdf_paths_old_1.append(pdf_path)
                if input(
                    "do you want to link this to Sorted Books? Yes(y), No(Any other key.)"
                ) in ["y", "य"]:
                    dest_of_link = input(
                        "enter the dir path to which you want to attach this pdf.\n"
                    )
                    if "'" in pdf_path:
                        os.system(f'ln -s "{pdf_path}" "{dest_of_link}"')
                    elif '"' in pdf_path:
                        os.system(f"ln -s '{pdf_path}' '{dest_of_link}'")
                    else:
                        os.system(f'ln -s "{pdf_path}" "{dest_of_link}"')
    print(f"number of deleted pdf till now is {len(list_of_deleted_pdf_paths_2)}")
    return size_of_delete_pdf_2


# delete pdf which were downloaded again by another downloader script.
def delete_again_undesired_pdfs(
    list_of_available_pdf_paths_new_2,
    list_of_deleted_pdf_paths,
    list_of_desired_pdf_paths,
    list_of_undesired_paths,
    size_of_delete_pdf,
    no_of_deleted_pdf
):
    # Iterate over list of available pdf paths.
    for i_n, each_pdf_path in enumerate(list_of_available_pdf_paths_new_2):
        # confirm that the pdf path is not present in list of desire pdf path and is not present in undesired dirs.
        if each_pdf_path not in list_of_desired_pdf_paths and all(
            each_string not in each_pdf_path for each_string in list_of_undesired_paths
        ):
            # print number of pdf....''
            print(i_n)
            # run a function to delete the pdf after due process of confirming.
            print(f"handing {each_pdf_path}")
            # get file size of this pdf in bytes and MB and truncated digits.
            # get pdf file size in bytes.
            pdf_file_size_raw = os.path.getsize(each_pdf_path)
            # convert size from bytes to MB
            pdf_file_size_MB = pdf_file_size_raw / (1024 * 1024)
            # truncate to 3 digits after decimal
            pdf_file_size = math.trunc(10**3 * pdf_file_size_MB) / 10**3
            print(f"size of this pdf is {pdf_file_size} MB.")
            # delete pdf
            # confirm that pdf still exists.
            if os.path.isfile(each_pdf_path):
                # if pdf is present in older list of deleted pdf paths, delete it again and warn to correct downloader scripts.
                if each_pdf_path in list_of_deleted_pdf_paths:
                    print(
                        f"{each_pdf_path}\t was already mentioned as undesired, so we are deleting it again. Check your download script which is downloading it again and again!!"
                    )
                    try:
                        os.remove(each_pdf_path)
                        if not os.path.isfile(each_pdf_path):
                            print("deleted it correctly.")
                            print(f'we freed {pdf_file_size} MB of space.')
                            no_of_deleted_pdf += 1
                            size_of_delete_pdf += pdf_file_size
                            print(f'we have delete total {no_of_deleted_pdf} pdf-s and total size of deleted pdf-s is :{size_of_delete_pdf}')
                        else:
                            print('we failed to delete this pdf.')
                    except Exception as x:
                        print(x)
                        print('we failed to delete this pdf.')
# 
# 
# 
def pickle_all(
    list_of_deleted_pdf_paths_1,
    deleted_file_paths_pickle_path_1,
    list_of_available_pdf_paths_1,
    available_file_paths_pickle_path_1,
    list_of_missing_pdf_paths_1,
    missing_file_paths_pickle_path_1,
    list_of_desired_pdf_paths_old_1,
    desired_file_paths_pickle_path_1,
):
    """AI is creating summary for pickle_all

    Args:
        deleted_file_paths_pickle_path_1 ([type]): [description]
        available_file_paths_pickle_path_1 ([type]): [description]
    """
    # print(deleted_file_paths_pickle_path_1)
    # print(desired_file_paths_pickle_path_1)
    try:
        with open(deleted_file_paths_pickle_path_1, "wb") as dfppp1:
            pickle.dump(list_of_deleted_pdf_paths_1, dfppp1)
        with open(available_file_paths_pickle_path_1, "wb") as afppp1:
            pickle.dump(list_of_available_pdf_paths_1, afppp1)
        with open(missing_file_paths_pickle_path_1, "wb") as mfppp1:
            pickle.dump(list_of_missing_pdf_paths_1, mfppp1)
        with open(desired_file_paths_pickle_path_1, "wb") as defppp1:
            pickle.dump(list_of_desired_pdf_paths_old_1, defppp1)
    except Exception as xxx_s:
        print(xxx_s)
        with open(deleted_file_paths_pickle_path_1, "wb") as dfppp1:
            pickle.dump(list_of_deleted_pdf_paths_1, dfppp1)
        with open(available_file_paths_pickle_path_1, "wb") as afppp1:
            pickle.dump(list_of_available_pdf_paths_1, afppp1)
        with open(missing_file_paths_pickle_path_1, "wb") as mfppp1:
            pickle.dump(list_of_missing_pdf_paths_1, mfppp1)
        with open(desired_file_paths_pickle_path_1, "wb") as defppp1:
            pickle.dump(list_of_desired_pdf_paths_old_1, defppp1)


def main(root_dir_2):
    """_summary_

    Args:
        root_dir_2 (_type_): _description_
    """
    # create a trash dir.
    trash_dir = f"{ROOT_DIR}_trash"
    # print(f'path of trash dir is {trash_dir}')
    if not os.path.isdir(trash_dir):
        os.makedirs(trash_dir)
    # Load old list of deleted pdf paths.
    deleted_file_paths_pickle_name = "pickle_of_list_of_deleted_pdf_paths"
    deleted_file_paths_pickle_path = os.path.join(
        DATA_ROOT_DIR, deleted_file_paths_pickle_name
    )
    if os.path.isfile(deleted_file_paths_pickle_path):
        with open(deleted_file_paths_pickle_path, "rb") as dfppp:
            list_of_deleted_pdf_paths = pickle.load(dfppp)
    else:
        list_of_deleted_pdf_paths = []
    print(f"All pdf deleted till now are {len(list_of_deleted_pdf_paths)}")
    # Load old list of available pdf paths
    available_file_paths_pickle_name = "pickle_of_list_of_all_pdf_paths"
    available_file_paths_pickle_path = os.path.join(
        DATA_ROOT_DIR, available_file_paths_pickle_name
    )
    if os.path.isfile(available_file_paths_pickle_path):
        with open(available_file_paths_pickle_path, "rb") as afppp:
            list_of_available_pdf_paths_old = pickle.load(afppp)
    else:
        list_of_available_pdf_paths_old = []
    print(f"total number of available pdf was {len(list_of_available_pdf_paths_old)}")
    # create a new list of available pdf paths
    print("creating a fresh list of available pdf paths afresh.")
    list_of_available_pdf_paths_new_2 = create_list_of_available_pdf_paths(
        root_dir_2, available_file_paths_pickle_path
    )
    print(f"total number of available pdf is {len(list_of_available_pdf_paths_new_2)}")
    # Load a list of pdf path which are missing or were not tracked while deleting.
    missing_file_paths_pickle_name = "pickle_of_list_of_missing_pdf_paths"
    missing_file_paths_pickle_path = os.path.join(
        DATA_ROOT_DIR, missing_file_paths_pickle_name
    )
    list_of_available_pdf_paths_new_2.sort()
    if os.path.isfile(missing_file_paths_pickle_path):
        with open(missing_file_paths_pickle_path, "rb") as mfppp:
            list_of_missing_pdf_paths_old = pickle.load(mfppp)
    else:
        list_of_missing_pdf_paths_old = []
    print(f"total number of missing pdf was {len(list_of_missing_pdf_paths_old)}")
    # create a new list of missing pdf paths
    print("checking for untracked deletions.")
    list_of_missing_pdf_paths_old_2 = make_a_list_of_non_tracked_missing_pdf(
        list_of_available_pdf_paths_old,
        list_of_missing_pdf_paths_old,
        missing_file_paths_pickle_path,
        trash_dir,
        list_of_deleted_pdf_paths,
    )
    # print(f'total number of missing pdf is {len(list_of_missing_pdf_paths_old_2)}')
    print(
        f"{len(list_of_missing_pdf_paths_old_2)} pdf were not tracked while deleting since last run."
    )
    # Load a list of pdf path which are desired and already confirmed as so.
    desired_file_paths_pickle_name = "pickle_of_list_of_desired_pdf_paths"
    desired_file_paths_pickle_path = os.path.join(
        DATA_ROOT_DIR, desired_file_paths_pickle_name
    )
    if os.path.isfile(desired_file_paths_pickle_path):
        with open(desired_file_paths_pickle_path, "rb") as mfppp:
            list_of_desired_pdf_paths = pickle.load(mfppp)
    else:
        list_of_desired_pdf_paths = []
    print(f"total number of confirmed desired pdf was {len(list_of_desired_pdf_paths)}")
    # delete pdf now
    delete_confirmation = input(
        "do you want to delete this pdf or to move to a separate trash dir. ? Delete(d), Move(any key)"
    )
    print("starting deletion of pdf...")
    # create similar path if needed
    create_same_folder_structure(ROOT_DIR, trash_dir)
    # defile dir path, which you don't want to check for undesire pdf....'
    list_of_undesired_paths = [
        "/Volumes/14TB_EXOS_28102020/archive.org/01_archive_downloader_config_data",
        "/Volumes/14TB_EXOS_28102020/archive.org/00_wget_commands",
        "/Volumes/14TB_EXOS_28102020/archive.org/01_archive_downloader_config_data",
        "/Volumes/14TB_EXOS_28102020/archive.org/01_corrupt_pdf_check_n_delete",
        "/Volumes/14TB_EXOS_28102020/archive.org/01-DownloadList",
        "/Volumes/14TB_EXOS_28102020/archive.org/02-DownloadScript",
        "/Volumes/14TB_EXOS_28102020/archive.org/03-Archive-wget",
        "/Volumes/14TB_EXOS_28102020/archive.org/archive.org_Folders",
    ]
    # 
    # 
    size_of_delete_pdf = 0
    no_of_deleted_pdf = 0
    # 
    print('checking if you have downloaded undesired pdf again, if yes then deleting them....')
    time.sleep(15)
    delete_again_undesired_pdfs(
        list_of_available_pdf_paths_new_2,
        list_of_deleted_pdf_paths,
        list_of_desired_pdf_paths,
        list_of_undesired_paths,
        size_of_delete_pdf,
        no_of_deleted_pdf
    )
    # 
    print('now we will check each pdf, ask you for desire/undesire, delete/keep and save details in database...')
    time.sleep(15)
    # counter for size of deleted pdf in this session.
    size_of_deleted_pdf = 0
    # Iterate over list of available pdf paths.
    for i_n, each_pdf_path in enumerate(list_of_available_pdf_paths_new_2):
        # confirm that the pdf path is not present in list of desire pdf path and is not present in undesired dirs.
        if each_pdf_path not in list_of_desired_pdf_paths and all(
            each_string not in each_pdf_path for each_string in list_of_undesired_paths
        ):
            try:
                # print number of pdf....''
                print(i_n)
                # run a function to delete the pdf after due process of confirming.
                size_of_deleted_pdf = delete_pdf(
                    each_pdf_path,
                    list_of_deleted_pdf_paths,
                    delete_confirmation,
                    list_of_desired_pdf_paths,
                    trash_dir,
                    list_of_deleted_pdf_paths,
                    size_of_deleted_pdf
                )
                pickle_all(
                    list_of_deleted_pdf_paths,
                    deleted_file_paths_pickle_path,
                    list_of_available_pdf_paths_new_2,
                    available_file_paths_pickle_path,
                    list_of_missing_pdf_paths_old_2,
                    missing_file_paths_pickle_path,
                    list_of_desired_pdf_paths,
                    desired_file_paths_pickle_path,
                )
            except Exception as x_s:
                print(x_s)
                print("now pickling all lists")
                pickle_all(
                    list_of_deleted_pdf_paths,
                    deleted_file_paths_pickle_path,
                    list_of_available_pdf_paths_new_2,
                    available_file_paths_pickle_path,
                    list_of_missing_pdf_paths_old_2,
                    missing_file_paths_pickle_path,
                    list_of_desired_pdf_paths,
                    desired_file_paths_pickle_path,
                )
        else:
            print(f"{each_pdf_path} was confirmed as desired in last run.")


if __name__ == "__main__":
    try:
        main(ROOT_DIR)
    except Exception as x_xs:
        print(x_xs)
        # pickle_all(
        #     list_of_deleted_pdf_paths,
        #     deleted_file_paths_pickle_path,
        #     list_of_available_pdf_paths_new_2,
        #     available_file_paths_pickle_path,
        #     list_of_missing_pdf_paths_old_2,
        #     missing_file_paths_pickle_path,
        #     list_of_desired_pdf_paths,
        #     desired_file_paths_pickle_path,
        # )
