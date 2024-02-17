import cv2

LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6
LEFT_ELBOW = 7
RIGHT_ELBOW = 8
LEFT_WRIST = 9
RIGHT_WRIST = 10
CHEST = 17

NODE_INDICES = [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, LEFT_WRIST, RIGHT_WRIST, CHEST]

NUM_MEASUREMENTS = 10
HEIGHT = 480
WIDTH = 640
TPOSE_THRESHOLD = 25
ANGLE_THRESHOLD = 35
CENTER_WIDTH = 640
CENTER_HEIGHT = 480


class Arm:
    def __init__(self):
        self._elbow = [0,0]
        self._wrist = [0,0]
        self._shoulder = [0,0]
        self._bicep = [0,0]
        self._forearm = [0,0]

    def is_horizontal(self, threshold=TPOSE_THRESHOLD):
        return (-threshold < self.bicep[1] < threshold) and (-threshold < self.forearm[1] < threshold)

    def angle_up(self, threshold=ANGLE_THRESHOLD):
        return (-threshold < self.bicep[1] < threshold) and (-threshold < self.forearm[0] < threshold) and (self.forearm[1] > 0)

    def angle_down(self, threshold=ANGLE_THRESHOLD):
        return (-threshold < self.bicep[1] < threshold) and (-threshold < self.forearm[0] < threshold) and (self.forearm[1] < 0)
        
    @property
    def wrist(self):
        return self._wrist

    @wrist.setter
    def wrist(self, wrist):
        self._wrist = wrist

    @property
    def elbow(self):
        return self._elbow

    @elbow.setter
    def elbow(self, elbow):
        self._elbow = elbow

    @property
    def shoulder(self):
        return self._shoulder

    @shoulder.setter
    def shoulder(self, shoulder):
        self._shoulder = shoulder

    @property
    def bicep(self):
        return [self.shoulder[0] - self.elbow[0], self.shoulder[1] - self.elbow[1]] 

    @property
    def forearm(self):
        return [self.elbow[0] - self.wrist[0], self.elbow[1] - self.wrist[1]] 


class Body:
    def __init__(self):
        self.right_arm = Arm()
        self.left_arm = Arm()
        self.chest = [WIDTH/2, HEIGHT/2]

    def t_pose(self):
        return self.left_arm.is_horizontal() and self.right_arm.is_horizontal()

    def m_pose(self):
        return self.left_arm.angle_down() and self.right_arm.angle_down()

    def w_pose(self):
        return self.left_arm.angle_up() and self.right_arm.angle_up()

    def s_pose(self):
        return (self.left_arm.angle_up() and self.right_arm.angle_down()) or (self.left_arm.angle_down() and self.right_arm.angle_up())

def classify_pose(peaks, counts, objects, topology, body):
    pose_classification = ""

    for i in range(counts[0]):
        pose = objects[0][i]
        # keypoints = np.array([peaks[0][j][pose[j]] for j in range(len(pose)) if pose[j] >= 0], dtype=object)
        
        # # Check if keypoints for required body parts were detected
        # if len(keypoints) < max(LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_ELBOW, RIGHT_ELBOW, RIGHT_WRIST, LEFT_WRIST) + 1:
        #     continue

        coords = list()
        chest_in_frame = False
        
        # Get the coordinates of each body parts in keys
        K = topology.shape[0]
        for i in range(counts[0]):
            obj = objects[0][i]
            for j in NODE_INDICES:
                k = int(obj[j])
                if k >= 0:
                    if j == CHEST:
                        chest_in_frame = True
                    peak = peaks[0][j][k]
                    x, y = int(peak[1] * WIDTH), int(peak[0] * HEIGHT)
                    coords.append([x,y])

        if len(coords) != len(NODE_INDICES):
            return "No Pose", chest_in_frame

        
        body.left_arm.shoulder = coords[0]
        body.right_arm.shoulder = coords[1]
        body.left_arm.elbow = coords[2]
        body.right_arm.elbow = coords[3]
        body.left_arm.wrist = coords[4]
        body.right_arm.wrist = coords[5]
        body.chest = coords[6]
        

        if body.t_pose():
            pose_classification = "T-Pose"
        elif body.m_pose():
            pose_classification = "M-Pose"
        elif body.w_pose():
            pose_classification = "W-Pose"
        elif body.s_pose():
            pose_classification = "S-Pose"
        else:
            pose_classification = "No Pose"

    return pose_classification, chest_in_frame


def draw_keypoints_and_values(image, counts, objects, peaks, topology):
    height, width = image.shape[:2]
    K = topology.shape[0]
    for i in range(counts[0]):
        obj = objects[0][i]
        C = obj.shape[0]
        for j in range(C):
            k = int(obj[j])
            if k >= 0:
                peak = peaks[0][j][k]
                x, y = int(peak[1] * width), int(peak[0] * height)
                cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
                # Display keypoint number and its coordinates
                keypoint_label = f"{j}:({x}, {y})"
                cv2.putText(image, keypoint_label, (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        for k in range(K):
            c_a = topology[k][2]
            c_b = topology[k][3]
            if obj[c_a] >= 0 and obj[c_b] >= 0:
                peak0 = peaks[0][c_a][obj[c_a]]
                peak1 = peaks[0][c_b][obj[c_b]]
                x0, y0 = int(peak0[1] * width), int(peak0[0] * height)
                x1, y1 = int(peak1[1] * width), int(peak1[0] * height)
                cv2.line(image, (x0, y0), (x1, y1), (255, 0, 0), 2)
