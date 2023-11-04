# This is a sample Python script.
import os
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess
import random
import pysrt


def get_duration_cmd_file(file):
    return f"""ffmpeg -i {file} 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,//"""


def cut_video(start_time, duration, input, output):
    return f"""ffmpeg -ss {start_time} -i {input} -t {duration} -c:v libx264 -c:a aac {output}"""


def merge_video(output, input_videos="merge.txt"):
    return f"""ffmpeg -f concat -safe 0 -i {input_videos} -c copy {output}"""


def execuateCmd(cmd, is_error_output=False):
    # status,output=subprocess.getstatusoutput(cmd);
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate()
    if (is_error_output):
        return proc.returncode, str(outs, encoding="utf-8") + "##" + str(errs, encoding="utf-8"), proc
    else:
        return proc.returncode, str(outs, encoding="utf-8"), proc


def main():
    # cut 多个不同视频，编解码还有问题，会出现黑屏卡顿bug，需先转化成同格式视频再裁剪
    # cut_merge_multi_videos()
    cut_merge_one_video("1.mp4")


def get_start_time(start):
    time_arr = ["0", "0", "0"]
    n = start
    index = 2
    while n > 0:
        result = n % 60
        time_arr[index] = str(result)
        index = index - 1
        n = int(n / 60)
        print(str(result))
    print(time_arr)
    return ":".join(time_arr)

def returnSeconds(subTime):
    return subTime.hours*3600 + subTime.minutes*60 + subTime.seconds + subTime.milliseconds / 1000

def readSRTFile(srt_file):
    subs = pysrt.open(srt_file)
    result = []
    for sub in subs:
        result.append(returnSeconds(sub.duration))
        print(sub.duration.to_time())
    print(result)
    return result
def cut_merge_one_video(file):
    os.chdir("videos3")
    execuateCmd("rm -rf cut")
    execuateCmd("mkdir cut")
    result = readSRTFile("1.srt")
    status, time, proc = execuateCmd(get_duration_cmd_file(file))
    print(time)
    print("--------")
    time_dur = 0
    index = 2
    for one in time.split(":"):
        time_dur = time_dur + pow(60, index) * float(one)
        index = index - 1
    print(time_dur)
    count = 0
    for item in result:
        cut_file = f"cut/{file}_cut{count}.mp4"
        start = random.randint(0, int(time_dur) - 8)
        print(start)
        start_time = get_start_time(start)
        print(start_time)
        cut_cmd = cut_video(start_time, item, file, cut_file)
        print(cut_cmd)
        execuateCmd(cut_cmd)
        count = count + 1
    os.chdir("cut")
    execuateCmd("cp ../../gen_merge_txt.sh .")
    execuateCmd("sh gen_merge_txt.sh")
    merge_cmd = merge_video("mergezms.mp4")
    print(merge_cmd)
    execuateCmd(merge_cmd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
