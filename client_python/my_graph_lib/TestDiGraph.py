from unittest import TestCase
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph

class TestDiGraph(TestCase):

    def make_my_graph(self):
        my_algo = GraphAlgo()
        my_algo.graph.add_node(0,(1.1, 1.5, 0))
        my_algo.graph.add_node(2,(1.4, 1.3 , 0))
        my_algo.graph.add_node(5,(1.1, 0.5, 0))
        my_algo.graph.add_node(6,(1.3, 1, 0))
        my_algo.graph.add_node(7,(1.5, 0.8, 0))
        my_algo.graph.add_node(10,(2.0, 1.1, 0))
        my_algo.graph.add_node(12,(2.5, 1.4, 0))
        my_algo.graph.add_node(13,(1.3, 0.3, 0))
        my_algo.graph.add_edge(0, 2, 1.2)
        my_algo.graph.add_edge(2, 0, 2.5)
        my_algo.graph.add_edge(2, 10, 1.8)
        my_algo.graph.add_edge(6, 2, 1.3)
        my_algo.graph.add_edge(6, 5, 1.4)
        my_algo.graph.add_edge(5, 7, 0.2)
        my_algo.graph.add_edge(7, 13, 2.6)
        my_algo.graph.add_edge(13, 10, 1.85)
        my_algo.graph.add_edge(10, 6, 1.1)
        my_algo.graph.add_edge(10, 7, 1.32)
        my_algo.graph.add_edge(10, 12, 1.0)
        my_algo.graph.add_edge(12, 13, 1.7)
        return my_algo

    def test_v_size(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A1.json")
        self.assertEqual(17, algo1.graph.v_size())
        algo1.load_from_json("..\\data\\A2.json")
        self.assertEqual(31, algo1.graph.v_size())
        algo1.graph.remove_node(0)
        self.assertEqual(30, algo1.graph.v_size())
        algo1.graph.add_node(0, (1,2,3))
        self.assertEqual(31, algo1.graph.v_size())
        algo1 = self.make_my_graph()
        self.assertEqual(8, algo1.graph.v_size())



    def test_e_size(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A1.json")
        self.assertEqual(36, algo1.graph.e_size())
        algo1.graph.remove_node(0)
        self.assertEqual(32, algo1.graph.e_size())
        algo1.graph.add_edge(0,1,4)
        self.assertEqual(32, algo1.graph.e_size())
        algo1.graph.add_node(0,(0,1,2))
        algo1.graph.add_edge(0,1,4)
        self.assertEqual(33, algo1.graph.e_size())
        algo1 = self.make_my_graph()
        self.assertEqual(12, algo1.graph.e_size())


    def test_all_in_edges_of_node(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A1.json")
        self.assertEqual(1.8635670623870366, algo1.graph.all_in_edges_of_node(0).get(1))
        algo1.graph.remove_edge(1,0)
        self.assertEqual(None, algo1.graph.all_in_edges_of_node(0).get(1))
        algo1.graph.remove_node(0)
        self.assertEqual(None, algo1.graph.all_in_edges_of_node(0))
        algo1 = self.make_my_graph()
        self.assertEqual(2, len(algo1.graph.all_in_edges_of_node(2)))




    def test_all_out_edges_of_node(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A1.json")
        self.assertEqual(2, len(algo1.graph.all_out_edges_of_node(0)))
        algo1.graph.remove_edge(0,16)
        self.assertEqual(1, len(algo1.graph.all_out_edges_of_node(0)))
        algo1 = self.make_my_graph()
        self.assertEqual(2, len(algo1.graph.all_out_edges_of_node(6)))
        self.assertEqual(None, algo1.graph.all_out_edges_of_node(45))



    def test_get_mc(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A2.json")
        self.assertEqual(111, algo1.graph.get_mc())
        algo1.graph.add_node(44, (0,1,2))
        self.assertEqual(112, algo1.graph.get_mc())
        algo1 = self.make_my_graph()
        self.assertEqual(20, algo1.graph.get_mc())
        algo1.graph.remove_node(0)
        self.assertEqual(25, algo1.graph.get_mc())


    def test_add_edge(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A3.json")
        self.assertEqual(136, algo1.graph.e_size())
        algo1.graph.add_edge(6,8, 23)
        self.assertEqual(137, algo1.graph.e_size())
        algo1 = self.make_my_graph()
        self.assertEqual(12, algo1.graph.e_size())
        algo1.graph.add_edge(0,5,12)
        self.assertEqual(13, algo1.graph.e_size())



    def test_add_node(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A2.json")
        self.assertEqual(31, algo1.graph.v_size())
        algo1.graph.add_node(44, (0,1,2))
        self.assertEqual(32, algo1.graph.v_size())
        algo1 = self.make_my_graph()
        self.assertEqual(8, algo1.graph.v_size())
        self.assertEqual(False, algo1.graph.add_node(0, (1.1, 1.5, 10)))


    def test_remove_node(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A1.json")
        self.assertEqual(17, algo1.graph.v_size())
        algo1.graph.remove_node(0)
        self.assertEqual(16, algo1.graph.v_size())
        self.assertEqual(False, algo1.graph.remove_node(0))
        algo1 = self.make_my_graph()
        self.assertEqual(8, algo1.graph.v_size())
        self.assertEqual(False, algo1.graph.remove_node(144))
        algo1.graph.remove_node(5)
        self.assertEqual(7, algo1.graph.v_size())

    def test_remove_edge(self):
        algo1 = GraphAlgo()
        algo1.load_from_json("..\\data\\A1.json")
        self.assertEqual(36, algo1.graph.e_size())
        algo1.graph.remove_edge(0,1)
        self.assertEqual(35, algo1.graph.e_size())
        self.assertEqual(False, algo1.graph.remove_edge(0,1))
        algo1 = self.make_my_graph()
        self.assertEqual(12,algo1.graph.e_size())
        algo1.graph.remove_edge(0,2)
        self.assertEqual(0, len(algo1.graph.all_out_edges_of_node(0)))
        self.assertEqual(1, len(algo1.graph.all_in_edges_of_node(0)))
        algo1.graph.remove_edge(2,0)
        self.assertEqual(0, len(algo1.graph.all_in_edges_of_node(0)))


