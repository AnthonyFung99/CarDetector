import cv2
import imutils
import os
import numpy
import pandas
from datetime import datetime
from tracker import Tracker

lines = []
draw = False
ix, iy = -1, -1
id_cnt = 1

class Line:
   def __init__(self, new_start, new_end):
       self.id = None
       self.start = new_start
       self.end = new_end
       self.total = 0
       self.countdown_frames = 0

       if ((new_start[1] > new_end[1] and (abs(new_start[0] - new_end[0]) < abs(new_start[1] - new_end[1]))) or
          (new_start[0] > new_end[0] and (abs(new_start[0] - new_end[0]) > abs(new_start[1] - new_end[1])))):
          self.start, self.end = self.end, self.start

   def check_box_line_interaction(self, box_top_left, box_bottom_right):
       if (self.start[0] >= box_bottom_right[0] or self.end[0] <= box_top_left[0]
           or self.start[1] >= box_bottom_right[1] or self.end[1] <= box_top_left[1]):
           return False
       else:
           return True

def draw_line(event, x, y, flagval, par):
   global draw, ix, iy, id_cnt

   if event == cv2.EVENT_LBUTTONDOWN:
       draw = True
       ix, iy = x, y

   elif event == cv2.EVENT_LBUTTONUP:
       draw = False
       cv2.line(image_window, (ix, iy), (x, y), (55, 55, 255), 3)
       line = Line((ix, iy), (x, y))
       line.id = id_cnt
       id_cnt += 1
       lines.append(line)
       print("Line start and end:", (ix, iy), (x, y))
       print("Updated Line start and end:", line.start, line.end)

cv2.namedWindow(winname="Image_Window")
cv2.setMouseCallback('Image_Window', draw_line)

videofile = 'intersection_video.mp4'
vidcap = cv2.VideoCapture(videofile)
success, first_frame = vidcap.read()
height, width, c = first_frame.shape
image_window = cv2.resize(first_frame, (1020, 700))

while vidcap.isOpened():
   cv2.imshow("Image_Window", image_window)
   if cv2.waitKey(1) & 0xFF == 27:
       break
   else:
       continue

vidcap.release()
cv2.destroyAllWindows()

track = Tracker()
last_frame = None

df = pandas.DataFrame(columns=['car_id', 'entry_line_id', 'entry_time', 'exit_line_id', 'exit_time', 'duration'])


cap = cv2.VideoCapture(videofile)
movement_track = []


while cap.isOpened():
   _, frame = cap.read()
   if frame is not None:
       frame = cv2.resize(frame, (1020, 700))
   else:
       break
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   blurred = cv2.GaussianBlur(gray, (9, 9), 1)


   if last_frame is None:
       last_frame = blurred
       continue

   delta_frame = cv2.absdiff(last_frame, blurred)
   last_frame = blurred

   kernel_frame = numpy.ones((5,5),numpy.uint8)
   thresh_frame = cv2.threshold(delta_frame, 30, 30, cv2.THRESH_BINARY)[1]
   thresh_frame = cv2.dilate(thresh_frame, kernel_frame, iterations=10)

   contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   contours = [c for c in contours if cv2.contourArea(c) > 6000 and cv2.contourArea(c) < 20000]

   for contour in contours:
       moment = cv2.moments(contour)
       movement_track.append([int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])])

   for moment_coordinates in movement_track:
        coordinate_x, coordinate_y = moment_coordinates
        cv2.line(frame, (coordinate_x, coordinate_y), (coordinate_x, coordinate_y), (0, 255, 255), 3)

   max_length = len(contours) * 40
   if len(movement_track) > max_length:
        movement_track = movement_track[-max_length:]

   detected_cars = [[coordinate_x, coordinate_y, width, height] for contour in contours for coordinate_x, coordinate_y, width, height in [cv2.boundingRect(contour)]]
   detected_cars_with_ids = track.update(detected_cars)


   fps = cap.get(cv2.CAP_PROP_FPS)


   for (coordinate_x, coordinate_y, width, height, car_id) in detected_cars_with_ids:
      
       cv2.putText(frame, "CAR", (coordinate_x, coordinate_y), cv2.FONT_ITALIC, 0.4, (0, 25, 255), 2)
       cv2.rectangle(frame, (coordinate_x, coordinate_y), (coordinate_x + width, coordinate_y + height), (0, 255, 0), 3)

       text = "Detected cars: " + str(len(contours)) + " || FPS: " + str(int(fps))
      
       for line in lines:
          
           if line.check_box_line_interaction((coordinate_x, coordinate_y), (coordinate_x + width, coordinate_y + height)):
               if line.countdown_frames <= 0:
                   line.total += 1
                   car_time = datetime.now()
                   print("Car with ID " + str(car_id) + " just passed the line " + str(line.id) + " at time: " + str(car_time))
                   if car_id in df['car_id'].values:
                       df.loc[df['car_id'] == car_id, 'exit_line_id'] = line.id
                       df.loc[df['car_id'] == car_id, 'exit_time'] = car_time
                       df.loc[df['car_id'] == car_id, 'duration'] = pandas.Timedelta(((car_time - df.loc[df['car_id'] == car_id]['entry_time']).values[0])).total_seconds()
                   else:
                       df.loc[car_id] = [car_id, line.id, car_time, None, None, None]
               line.countdown_frames = 20
           else:
               line.countdown_frames -= 1
          
           text += " (Line ID: " + str(line.id) + ", Total Cars: " + str(line.total) + ", Countdown Frames: " + str(line.countdown_frames) + ")"
    
   cv2.rectangle(frame, (0, 0), (1020, 30), (0, 0, 0), -1)
   cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

   for line in lines:
       cv2.line(frame, line.start, line.end, (55, 55, 255), 2)
       cv2.putText(frame, "Line id:" + str(line.id), (line.start[0], line.start[1] - 10), cv2.FONT_ITALIC, 0.6, (55, 55, 255), 2)


   for coordinate_x, coordinate_y, _, _, id in detected_cars_with_ids:
       cv2.putText(frame, "ID:" + str(id), (coordinate_x, coordinate_y - 15), cv2.FONT_ITALIC, 0.6, (0, 255, 0), 2)
       cv2.imshow("Cars", frame)


   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

cap.release()
cv2.destroyAllWindows()

csv_file, _ = os.path.splitext(videofile)
df.to_csv(f"{csv_file}_table.csv", index=False)