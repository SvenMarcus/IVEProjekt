from typing import List


class TrackList:

    def __init__(self, trackData: List[List[str]]):
        self.__trackData: List[List[str]] = trackData

    def getTrackWith(self, start: str, end: str) -> List[str]:
        for track in self.__trackData:
            if len(track) < 3:
                continue

            if track[0] == start and track[2] == end:
                return track
        return []
