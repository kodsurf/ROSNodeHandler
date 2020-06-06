import rospy
from geometry_msgs.msg import *
from sensor_msgs.msg import *


class NodeHandler():
	messages = {}
	publishers = {}
	subscriberCallbacks = {}
	subscribers =[]


	def __init__(self, nodeName,inputMsgs,pubTopics):
		

		def makeCalbacFunction(topicName):
			def f(data):
				self.messages[topicName]=data
				vars(self)[topicName] = data
				print "callbackF = "+topicName
			return f

		rospy.init_node(nodeName) #initialize node
		#create variables to store received messages
		for topicName in inputMsgs:
			self.messages.update({
				#topicName:inputMsgs[topicName]
				topicName:None #initialize None
				})
			print "Message variable "+str(topicName)+" initialized : "+ str(self.messages[topicName])


		#creare properly named message names
		for topicName in inputMsgs:
			vars(self)[topicName] = self.messages[topicName]
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
			#print publisherName
			pub = rospy.Publisher(key, type(pubTopics[key]), queue_size=10)
			#print key, type(inputMsgs[key])
			vars(self)[publisherName] = pub
			self.publishers.update({
				key:pub
				})
			print "Publisher : "+publisherName+" initialized "+str(vars(self)[publisherName])
		#create properly named get wait functions

		for topicName in inputMsgs:
			self.__MakeNamedGets(topicName)
		
	
	def __MakeNamedGets(self,topicName):
		functionName = "get_"+str(topicName)
		#print functionName

		
		def get():
				self.messages[topicName]=None
				vars(self)[topicName] = None
				r = rospy.Rate(10)
				while not rospy.is_shutdown():
					print "GET WAITING = "+topicName
					if self.messages[topicName] is None or vars(self)[topicName] is None:
						r.sleep()
						continue
					ret = self.messages[topicName]
					break
				return ret
		vars(self)[functionName]=get
		#print vars(self)
		#self.get_func()
	def NodeInfo(self):
		print "Node info :"
		#print vars(self)
		print "SUBSCTIBERS :::::::"
		subs = []

		for subscribersName in self.messages:
			#print subscribersName
			subs.append(subscribersName)
		print subs

		print "PUBLISHERS::::"
		pubs = []
		for publisherName in self.publishers:
			pubs.append(publisherName)
			#print publisherName
		print pubs
		return subs,pubs

	

def main():
	# DEFINE TOPICS FOR SUBSCRIPTION   key= Topic    Value = message type

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
	subs, pubs =n.NodeInfo()





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