import unittest

from hw5 import *

# test file for homework 5

LOCAL_TIMEOUT = 10

class tester_add_position(unittest.TestCase):
	def test__given(self):
		#add_position(head, data, position)
		
		a = Node(2, Node(3, Node(4, Node(6))))
		a = add_position(a, 5, 3)
		self.assertEqual(a.next_node.next_node.next_node.data, 5)
		
		a = add_position(a, 1, 0)
		self.assertEqual(a.data, 1)


		a = Node(2, Node(3))
		a = add_position(a, 8, 0)
		self.assertEqual(a.data, 8)



class tester_remove_position(unittest.TestCase):

	def test__given(self):
		a = Node(2, Node(3, Node(4)))
		a = remove_position(a, 1)
		self.assertEqual(a.next_node.data, 4)

		a = Node(2, Node(3, Node(4)))
		a = remove_position(a, 0)
		self.assertEqual(a.data, 3)

	def test_vacuous_given(self):
		#if head is none
		self.assertIsNone(None, 1)	


class tester_merge(unittest.TestCase):
	def test_given(self):
		head_a = Node(2, Node(3))
		head_b = Node(1, Node(4))
		head_result = merge_lists(head_a, head_b)
		self.assertEqual(head_result.data, 1)
		self.assertEqual(head_result.next_node.data, 2)
		self.assertEqual(head_result.next_node.next_node.data, 3)
		self.assertEqual(head_result.next_node.next_node.next_node.data, 4)



class tester_reverse_list(unittest.TestCase):

	def test_given(self):
		a = Node(2, Node(3, Node(4)))
		reversed = reverse_list(a)
		self.assertEqual(reversed.data, 4)
		self.assertEqual(reversed.next_node.data, 3)
		self.assertEqual(reversed.next_node.next_node.data, 2)


		self.assertIsNone(reverse_list(None))
	



class tester_find_merge_point(unittest.TestCase):
	
	def test__given(self):
		a = Node(2, Node(6, Node(-8)))
		a1 = Node(3, a)
		a2 = Node(5, a)
		
		self.assertEqual(find_merge_point(a1, a2), 2)

		a3 = Node(6)
		self.assertIsNone(find_merge_point(a3, a2))
	

class tester_find_cycle(unittest.TestCase):
	
	def test__given(self):
		node_a = Node(1)
		node_b = Node(2)
		node_c = Node(3)
		
		node_a.next_node = node_b
		node_b.next_node = node_c
		
		# create cycle between node_b and node_b
		node_c.next_node = node_b

		self.assertTrue(find_cycle(node_a))
	




#===================================

# suppress stdout, but keep stderr since that's what unittest uses
# https://stackoverflow.com/questions/30715337

from io import StringIO
import sys

class ReplaceStd(object):
	""" Let's make it pythonic. """

	def __init__(self):
		self.stdout = None
		#self.stderr = None

	def __enter__(self):
		self.stdout = sys.stdout
		#self.stderr = sys.stderr

		# as it was suggested already:
		sys.stdout = StringIO()
		#sys.stderr = StringIO()

	def __exit__(self, type, value, traceback):
		sys.stdout.close()
		#sys.stderr.close()
		
		sys.stdout = self.stdout
		#sys.stderr = self.stderr

if __name__ == "__main__":
	
	with ReplaceStd():
		unittest.main(module=__name__, buffer=True, exit=False)
	
