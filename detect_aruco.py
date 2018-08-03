import numpy
import cv2
import cv2.aruco as aruco

# constants
num_rows = 7
num_cols = 4
# boundary ids
boundary_ids = [16,17,18,19]
order_of_corners = [2,1,0,3]
obs_id = [0,3,4,5]
obs = [None, None, None, None]
start_id = 6
start = None
goal_id = 7
goal = None

return_dat_boi = {"obs": [], "start": [], "end": []}

grid_line_rows = []
grid_line_cols = []
# initialize the row, col list
for i in range(num_rows-1):
	grid_line_rows.append(None)
for j in range(num_cols-1):
	grid_line_cols.append(None)

class line:
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.slope = (end[1]-start[1])/(end[0]-start[0])


# helper functions
def get_avg_coord(boi):
	x_avg = 0
	y_avg = 0 
	for x,y in boi: # the box
		x_avg += x/4
		y_avg += y/4

	return (x_avg, y_avg)

# generates 500px images of aruco markers
def create_aruco():
	dictionary = aruco.getPredefinedDictionary(0)
	for boi in range(50):
		img = aruco.drawMarker(dictionary, boi, 500)
		cv2.imwrite("aruco_4x4_" + str(boi) + ".jpg", img)

cap = cv2.VideoCapture(0)

def main_boi():
	while(True):
		ret, frame = cap.read()

		#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		aruco_dict = aruco.getPredefinedDictionary(0)
		parameters =  aruco.DetectorParameters_create()

		# draw boundary
		cv2.rectangle(frame, (50,50), (1230,670), (255,0,0),2 )

		corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
		for box_index in range(len(corners)):
			
			x_avg = get_avg_coord(corners[box_index][0])[0]
			y_avg = get_avg_coord(corners[box_index][0])[1]
			
			cv2.rectangle(frame, (int(x_avg),int(y_avg)), (int(x_avg+5),int(y_avg+5)), (0,255,0),2)
			# if start
			if ids[box_index][0] == start_id:
				start = corners[box_index][0]
				print "start: " + str(get_aav_coord(start))
			
			# if goal
			elif ids[box_index][0] == goal_id:
				goal = corners[box_index][0]
				print "goal: " + str(get_avg_coord(goal))

			# if obs
			for i in range(len(obs_id)):
				if ids[box_index][0] in obs_id:
					obs[i] = get_avg_coord(corners[box_index][0])
					print "obs: " + str(obs)


			cv2.putText(frame,"id="+str(ids[box_index][0])+" ("+str(int(x_avg))+","+str(int(y_avg))+")", (int(x_avg),int(y_avg)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))

	 
		gray = aruco.drawDetectedMarkers(frame, corners)
		
		draw_grid(frame, num_rows, num_cols, corners, ids)

		# Display the resulting frame
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

def draw_grid(frame, row, col, corners, ids):
	# draw field boundaries

	# this is a list of the corner markers' coordinates
	field_boxes = []
	field_corners = []

	if ids is not None:
		# for the 4 corners
		for i in range(4):
			# for the elements in ids
			for id_index in range(len(ids)):
				# if the id is the ith element of the boundary, add to field boundaries
				if ids[id_index][0] == boundary_ids[i]:
					field_boxes.append(corners[id_index])

	# add box corners to the list
	if field_boxes:
		n = 0
		for box in field_boxes:
			field_corners.append((box[0][order_of_corners[n]][0],box[0][order_of_corners[n]][1]))
			n += 1

	# draw lines
	for field_corners_index in range(len(field_corners)):
		cv2.line(frame, field_corners[field_corners_index-1], field_corners[field_corners_index], (0,255,0))


	# draw grid lines
	if len(field_corners) == 4:
		# calculate (xdist ,ydist) between lines
		row_x_dist, row_y_dist = [(field_corners[1][0] - field_corners[0][0])/num_rows,(field_corners[1][1] - field_corners[0][1])/num_rows]
		col_x_dist, col_y_dist = [(field_corners[3][0] - field_corners[0][0])/num_cols,(field_corners[3][1] - field_corners[0][1])/num_cols]

		for i in range(num_rows-1):
			p1 = ( int(field_corners[0][0]+row_x_dist*(i+1)),int(field_corners[0][1]+row_y_dist*(i+1)) )
			p2 = ( int(field_corners[3][0]+row_x_dist*(i+1)),int(field_corners[3][1]+row_y_dist*(i+1)) )
			cv2.line(frame, p1, p2,(0,255,0))
			grid_line_rows[i] = [p1,p2]

		for j in range(num_cols-1):
			p1 = ( int(field_corners[0][0]+col_x_dist*(j+1)),int(field_corners[0][1]+col_y_dist*(j+1)) )
			p2 = ( int(field_corners[1][0]+col_x_dist*(j+1)),int(field_corners[1][1]+col_y_dist*(j+1)) )
			cv2.line(frame, p1, p2,(0,255,0))
			grid_line_cols[j] = [p1,p2]

	# find the points and where they lie


# def find_loc(frame, row, col, corners, ids):
# 	# find start
# 	for i in range(num_rows-1):
# 		for j in range(num_cols-1):


# 	# find goal
# 	for 
# 	# find obstacles
# 	if 
# 	for 
	


main_boi()
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

