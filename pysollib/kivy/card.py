#!/usr/bin/env python
# -*- mode: python; coding: utf-8; -*-
# ---------------------------------------------------------------------------#
#
# Copyright (C) 1998-2003 Markus Franz Xaver Johannes Oberhumer
# Copyright (C) 2003 Mt. Hood Playing Card Co.
# Copyright (C) 2005-2009 Skomoroh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------#

from pysollib.acard import AbstractCard
from pysollib.kivy.LApp import LImageItem
from pysollib.kivy.LImage import LImage
from pysollib.kivy.tkcanvas import MfxCanvasImage


class _HideableCard(AbstractCard):
    def hide(self, stack):
        if stack is self.hide_stack:
            return

    def unhide(self):
        if self.hide_stack is None:
            return 0
        return 1

    # moveBy aus Basisklasse überschreiben.
    def moveBy(self, dx, dy):
        # wir verwenden direkt den float Wert.
        if dx or dy:
            self.x = self.x + dx
            self.y = self.y + dy
            self.item.move(dx, dy)


# ************************************************************************
# * New implemetation since 2.10
# *
# * We use a single CanvasImage and call CanvasImage.config() to
# * turn the card.
# * This makes turning cards a little bit slower, but dragging cards
# * around is noticeable faster as the total number of images is
# * reduced by half.
# ************************************************************************
# * Kivy Implementation
# * Wir verwenden ein BoxLayout und installieren je nach Status das
# * face oder das back Image.
# ************************************************************************


class _OneImageCard(_HideableCard):
    def __init__(self, id, deck, suit, rank, game, x=0, y=0):
        _HideableCard.__init__(self, id, deck, suit, rank, game, x=x, y=y)

        fimage = game.getCardFaceImage(deck, suit, rank)
        bimage = game.getCardBackImage(deck, suit, rank)

        self._face_image = LImage(texture=fimage.texture)
        self._back_image = LImage(texture=bimage.texture)

        aimage = LImageItem(
            pos=(x, -y), size=self._face_image.size, game=game, card=self)
        aimage.add_widget(self._back_image)
        self._active_image = aimage

        self.item = MfxCanvasImage(
            game.canvas, self.x, self.y, image=aimage, anchor="nw")

        # print ('card: face = %s xy=%s/%s' % (self._face_image.source, x, y))
        # print ('card: back = %s xy=%s/%s' % (self._back_image.source, x, y))
        # y = self.yy

    def _setImage(self, image):
        self._active_image.clear_widgets()
        self._active_image.add_widget(image)

    def showFace(self, unhide=1):
        # print ('card: showFace = %s' % self._face_image.source)
        if not self.face_up:
            self._setImage(image=self._face_image)
            self.tkraise(unhide)
            self.face_up = 1

    def showBack(self, unhide=1):
        # print ('card: showBack = %s' % self._back_image.source)
        if self.face_up:
            self._setImage(image=self._back_image)
            self.tkraise(unhide)
            self.face_up = 0

    def updateCardBackground(self, image):
        print('card: updateCardBackground = %s' % image.source)
        self._back_image = LImage(texture=image.texture)
        if not self.face_up:
            self._setImage(image=self._back_image)

    '''
    def setSelected(self, s, group=None):
        print('card: setselected(%s, %s)' % (s, group))
        # wird nicht bedient.
        # NOTE:
        # This is one of the zombie methods (nowhere impelemeted: close,
        # unclose, and somewhat dummy implemented ones: hide, unhide)
        # of the base class AbstractCard.
        # (-> some clean ups for clarity would be nice)
        pass
    '''

    def animatedMove(self, dx, dy, duration=0.2):
        self.item.animatedMove(dx, dy, duration)


Card = _OneImageCard

'''end of file'''
