#!/usr/bin/env python
import rospy
from geometry_msgs.msg import *
from sensor_msgs.msg import *


class NodeHandler():

	subscriberCallbacks = {}
	subscribers =[]


	def __init__(self, nodeName,inputMsgs,pubTopics):
		

		def makeCalbacFunction(topicName):
			def f(data):
				vars(self)[topicName] = data
				print "callbackF = "+topicName
			return f

		rospy.init_node(nodeName) #initialize node

		#creare properly named message names
		for topicName in inputMsgs:
			vars(self)[topicName] = None
			print "Proper name  "+str(topicName)+" initialized : "+ str(vars(self)[topicName])
		


		#create callback functions for subscribers
		for topicName in inputMsgs:
			f = makeCalbacFunction(topicName)
			
			self.subscriberCallbacks.update({
				topicName:f
				})
		#create subscribers
		for topicName in inputMsgs:
			s = rospy.Subscriber(topicName,type(inputMsgs[topicName]), self.subscriberCallbacks[topicName])
			self.subscribers.append(s)
			print "Subscriber created : "+str(s)

		#create publishers
		for key in pubTopics:
			publisherName = "pub_"+key
			pub = rospy.Publisher(key, type(pubTopics[key]), queue_size=10)
			vars(self)[publisherName] = pub
			print "Publisher : "+publisherName+" initialized "+str(vars(self)[publisherName])
		
		#create properly named get wait functions
		for topicName in inputMsgs:
			self.__MakeNamedGets(topicName)
		
	
	def __MakeNamedGets(self,topicName):
		functionName = "get_"+str(topicName)

		def get():
				#self.messages[topicName]=None
				vars(self)[topicName] = None
				r = rospy.Rate(10)
				while not rospy.is_shutdown():
					print "GET WAITING = "+topicName
					if vars(self)[topicName] is None:
						r.sleep()
						continue
					ret = vars(self)[topicName]
					break
				return ret
		vars(self)[functionName]=get

	

def main():
	# DEFINE TOPICS FOR SUBSCRIPTIONS AND PUBLISHING  key= Topic    Value = message type

	subTopics = {
		"gnss_pose":PoseStamped(),
		"ndt_pose":PoseStamped(),
		"imu_raw":Imu(),
		"fix":NavSatFix(),
	}

	# DEFINE TOPICS YOU WISH TO PUBLISH
	pubTopics = {
		"relative_pose":PoseStamped(),
		"obstacle_pose":PoseStamped(),

	}

	#INITIALIZE NODE
	n = NodeHandler("NodeHandlerTest",subTopics,pubTopics)

	# MAIN ROS LOOP WITH LOGICS IMPLEMENTED
	while not rospy.is_shutdown():


		print "WAITING FOR FIX -----------------------------"
		msg = n.get_fix()
		print msg
		print "FIX RECEIVED"

		print "WAITING FOR NDT_POSE ----------------------"
		msg = n.get_ndt_pose()
		print msg
		print "NDT_POSE RECEIVED"

		print "NDT_POSE callback value -----------"
		print n.ndt_pose

		print "GNSS_POSE callback value ------------"
		print n.gnss_pose


		print "FIX CALBACK ----------"
		print n.fix


		print "DEMO ERROR  - PRINTING NONE EXISTENT VARIABLE"
		#print n.hh

		print "NOW LETS PUBLISH SOME MESSAGES _________________"
		m = PoseStamped()
		n.pub_relative_pose.publish(m)
		n.pub_obstacle_pose.publish(m)
		print "messages PUBLISHED ---------------"



if __name__ == "__main__" :
	main()