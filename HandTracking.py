import mediapipe

# This object creates a list from medipipe result set
# List holds landmarks' coordinates
class HandTracker:
	def __init__(self):
		pass
	# New result loaded on new frame
	def load_results(self, results):
		self.results = results

	# Get results and return a landmark list for five finger tips
	def get_hand_coordinates(self):
		markList = list()
		if self.results.multi_hand_landmarks:
			hand = self.results.multi_hand_landmarks[0]
			for id, mark in enumerate(hand.landmark):
				x_pix , y_pix = int(mark.x * 640), int(mark.y * 480)
				markList.append([id, x_pix, y_pix])

		return markList

	# Check if all finger tips are in the frame
	def check_fingers(self, markList, borders):
		for i in range(4,21,4):
			#if markList[i][1] > 640 or  markList[i][2] > 480 or markList[i][1] < 0 or markList[i][2] < 0:
			if (markList[i][1] < borders[0]) or  (markList[i][2] < borders[1]) or (markList[i][1] > borders[2]) or (markList[i][2] > borders[3]):
				return False

		return True