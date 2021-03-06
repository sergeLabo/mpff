#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## tempo.py

#############################################################################
# Copyright (C) Labomedia October 2016
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

'''
Class utilisable pour des tempo et compteur
'''


class TempoFactory():
    """Les tempos sont en fait des compteurs qui sont mis à jour à chaque
    frames de Blender avec update.
    """

    def __init__(self, periode=60):
        '''Paramètres:
    période: la tempo est remise à zéro si periode atteind, -1 = infinite loop
    pas: incrément de la tempo, par défaut=1, aucun intérêt de changer le pas
    verrou: si verrou, pas d'incrémentation.
    '''

        self.periode = periode
        self.verrou = False
        self.pas = 1
        self.tempo = 0

    def lock(self):
        '''Verrou, je bloque'''

        self.verrou = True

    def unlock(self):
        '''Pas de verrou, je peux incrémenter'''

        self.verrou = False

    def reset(self):
        '''Remise à zéro de la tempo'''

        self.tempo = 0

    def update(self):
        '''J'incrémente si pas de verrou. Si verrou, je ne fais rien'''

        if not self.verrou:
            self.tempo += self.pas
            if self.periode != -1:
                if self.tempo >= self.periode +1:
                    self.tempo = 0
        return self.tempo


class Tempo(dict):
    ''' Création des tempos définies dans une liste de tuple:
            * tempo_liste = [("intro", 60), ("print", 12), ("sound", 6)]
        Chaque objet tempo:
            * tempoDict = Tempo(tempo_liste)
        Update des tempo:
            * tempoDict.update()
        Appel d'une tempo:
            * tempoDict["intro"].tempo
        Voir exemple test() du __main__
    '''
    def __init__(self, tempoList):
        self.tempoList = tempoList
        for t in self.tempoList:
            self[t[0]] = TempoFactory(t[1])

    def update(self):
        for t in self.tempoList:
            self[t[0]].update()

class VirtualGl():
    ''' Classe vide pour simuler
    from bge import logic as gl
    Dommage que ça ne serve pas à grand chose
    '''
    pass



if __name__ == "__main__":
    # Only to test
    from time import sleep

    def test():
        gl = VirtualGl

        # Création de gl virtuel et variable intit
        gl = VirtualGl()
        gl.init_tempo = False

        while True:
            # Simulation de la pulsation de Blender à 60 fps
            sleep(0.5)
            if not gl.init_tempo:
                # Création des objects
                tempo_liste = [("intro", 60), ("print", 12), ("sound", 6)]
                tempoDict = Tempo(tempo_liste)
                print(tempoDict)
                gl.init_tempo = True

            if gl.init_tempo:
                # Incrémentation de toutes les tempos, sauf les locked
                tempoDict.update()

                # Début des tests
                if tempoDict["intro"].tempo == 12:
                    tempoDict["print"].lock()
                if tempoDict["intro"].tempo == 24:
                    tempoDict["print"].unlock()
                if tempoDict["intro"].tempo == 30:
                    tempoDict["print"].reset()

            print(tempoDict["intro"].tempo, tempoDict["print"].tempo,
                                                tempoDict["sound"].tempo)

    test()
