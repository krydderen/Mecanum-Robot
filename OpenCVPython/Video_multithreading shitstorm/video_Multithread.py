import cv2
import argparse
import os
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow


def putIterationsPerSecond(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of the frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
                (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0))
    return frame


# def noThreading(source=0):
#     """ Grap and show video frames without multithreading."""

#     cap = cv2.VideoCapture(source)
#     cap.set(3, 640)
#     cap.set(4, 480)
#     cap.set(10, 100)
#     cps = CountsPerSec().start()

#     while True:
#         (grabbed, frame) = cap.read()
#         frame = putIterationsPerSecond(frame, cps.CountsPerSec())
#         cv2.imshow("Video", frame)
#         cps.increment()
#         if cv2.waitKey(1) == ord("q"):
#             cv2.destroyAllWindows()
#             break


# def threadVideoGet(source=0):
#     """
#     Dedicated thread fro grabbing video frams with VideoGet object.
#     Main thread shows video frames.
#     """

#     video_getter = VideoGet(source).start()
#     cps = CountsPerSec()
#     cps.start()

#     while True:
#         frame = video_getter.frame
#         frame = putIterationsPerSecond(frame, cps.CountsPerSec())
#         cv2.imshow("Video", frame)
#         cps.increment()

#         if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
#             video_getter.stop()
#             cv2.destroyAllWindows()
#             break


# def threadVideoShow(source=0):
#     """
#     Dedicated thread for showing video frames with VideoShow object.
#     Main thread grabs video frames.
#     """
#     cap = cv2.VideoCapture(source)
#     (grabbed, frame) = cap.read()
#     video_shower = VideoShow(frame).start()
#     cps = CountsPerSec().sec()

#     while True:
#         (grabbed, frame) = cap.read()
#         if not grabbed or video_shower.stopped:
#             video_shower.stop()
#             cv2.destroyAllWindows()
#             break
#         frame = putIterationsPerSecond(frame, cps.CountsPersec())
#         video_shower.frame = frame
#         cps.increment()


def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and 
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSecond(frame, cps.CountsPerSec())
        video_shower.frame = frame
        cps.increment()


def main():
    threadBoth()


if __name__ == "__main__":
    main()
