'''
Joan La Rosa Ferre
Crossmint Interview 4/25/2022
'''

import os
import requests
from dotenv import load_dotenv
from typing import List


class CrossMintInterview:
    '''
    Althought there are many ways to interpret the problem, I chose to use a dictionary to store the data.
    '''

    def __init__(self, candidateId) -> None:
        self.url = 'https://challenge.crossmint.io/api/'
        self.candidateId = candidateId
        self.astr_obj = ['polyanets', 'soloons', 'comeths']
        self.map_to_astral_objects = {
            "POLYANET": 'polyanets', "SOLOON": 'soloons', "COMETH": 'comeths'}

    @property
    def goal(self) -> List[List[str]]:
        """
        The goal is a list of lists. Each list represents a row. Each row is an astral objects.
        Notice the format of the goal is {DATA}_{TYPE} Where DATA is the attribute of the TYPE.
        E.g PURPLE_SOLOON.
        """
        goalUrl = f'{self.url}map/{self.candidateId}/goal'
        response = requests.get(
            url=goalUrl,
            data={'candidateId': self.candidateId}
        )
        if 'goal' in response.json():
            return response.json()['goal']
        else:
            raise Exception(f'Not able to get goal from {goalUrl}')

    def setAstralObject(self, astral_obj: str, row: int, column: int, attr: dict = {}) -> None:
        """
        Set the astral object at the given row and column.
        Based on https://challenge.crossmint.io/documentation
        """
        if astral_obj not in self.astr_obj:
            raise Exception(
                f'Astral object {astral_obj} not in {self.astr_obj}')

        response = requests.post(
            url=self.url + astral_obj,
            data={'candidateId': self.candidateId,
                  'row': row, 'column': column,
                  **attr}
        )
        if response.status_code != 200:
            raise Exception(f'Not able to set {astral_obj} at {row}, {column}')

    def removeAstralObject(self, astral_obj: str, row: int, column: int) -> None:
        """
        Remove the astral object at the given row and column.
        Based on https://challenge.crossmint.io/documentation
        """
        if astral_obj not in self.astr_obj:
            raise Exception(
                f'Astral object {astral_obj} not in {self.astr_obj}')

        response = requests.delete(
            url=self.url + astral_obj,
            data={'candidateId': self.candidateId,
                  'row': row, 'column': column}
        )
        if response.status_code != 200:
            raise Exception(
                f'Not able to remove {astral_obj} at {row}, {column}')

    def solve(self):
        """
        Solve the puzzle 1 and 2.
        """
        goal = self.goal
        # print(f"{goal=}")
        for r, row in enumerate(goal):
            for c, obj in enumerate(row):
                astral_obj = obj.split("_")[-1]
                if astral_obj in self.map_to_astral_objects:
                    attr = {}
                    if astral_obj == "SOLOON":
                        attr['color'] = obj.split("_")[0].lower()
                    elif astral_obj == "COMETH":
                        attr['direction'] = obj.split("_")[0].lower()

                    self.setAstralObject(
                        self.map_to_astral_objects[astral_obj], r, c, attr)


if __name__ == '__main__':
    load_dotenv()
    CANDIDATE_ID = os.getenv('CANDIDATE_ID')
    c = CrossMintInterview(CANDIDATE_ID)
    c.solve()
