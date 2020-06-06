# ROSNodeHandler

To simplify initialization and usage of ROS nodes, publishers, subscribers.

To avoid defining callback functions for every subscriber in a node

Usage :

1)define topics you wish to subscribe to as dict

subTopics = {
		"gnss_pose":PoseStamped(),
		"ndt_pose":PoseStamped(),
		"imu_raw":Imu(),
		"fix":NavSatFix(),
	}
  
2) define topics you wish to publish to as dict

	pubTopics = {
		"relative_pose":PoseStamped(),
		"obstacle_pose":PoseStamped(),

	}
  
3) Initialize node with desired name
n = NodeHandler("NodeHandlerTest",subTopics,pubTopics)


4)Get messages from topics - 
4.1) Wait for new message syntax : "get_(topicName)"
msg = n.get_fix()
4.2) Access last received message : (topicName)
msg = n.fix

5) Publish    pub_topicName.publish()
m = PoseStamped()
n.pub_relative_pose.publish(m)
