# coding: utf-8
from BaseController import *
from lib.SiftMatch import *
import numpy as np
import conf.Config as conf
import urllib2 as url
import os

class AreaExceptionDetectController(BaseController):
	def execute(self):
		AreaExceptionDetectController.checkParams(self)
		if not self.imgDestUrl:
			rawData = self.processUpFile("imgDest")
		else:
			# 从其他地方获取图片
			rawData = url.urlopen(self.imgDestUrl).read()
		imgDest = cv2.imdecode(np.fromstring(rawData, np.uint8), cv2.IMREAD_COLOR)# IMREAD_COLOR
		imgFeature = cv2.imread("resources/" + self.imgFeature)
		H, W, _ = imgDest.shape
		# boundingBox = siftMatchVertical(imgFeature, imgDest)
		boundingBox = siftMatchVertical(imgFeature, imgDest, windowHeightRate = 0.05, method = "SIFT", resizeScale = 1, showImg = False)
		if boundingBox is not None and len(boundingBox) != 0:
			boundingBox[:, :, 0] = boundingBox[:, :, 0] / float(W)
			boundingBox[:, :, 1] = boundingBox[:, :, 1] / float(H)
			self.setResult(boundingBox.tolist(), STATUS_OK)
		else:
			self.setResult([], STATUS_SCAN_ERROR)

	@staticmethod
	def checkParams(self):
		whRatio = self.getIntArg("whRatio")
		imgFeature = self.getStrArg("imgFeature").strip()
		if whRatio == -1:
			raise ErrorStatusException("whRatio must be a float number", STATUS_PARAM_ERROR)
		if imgFeature == "" or not os.path.exists("resources/" + imgFeature):
			raise ErrorStatusException("imgFeature must be a valid resource name", STATUS_PARAM_ERROR)
		if not self.fileExist("imgDest"):
			self.imgDestUrl = self.getStrArg("imgDest")
		else:
			self.imgDestUrl = None
		self.imgFeature = imgFeature
		self.whRatio = whRatio

