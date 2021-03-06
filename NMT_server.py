import SocketServer
import sys
import logging
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from SimpleXMLRPCServer import SimpleXMLRPCServer

SRC_LANG = 'en'
TGT_LANG = 'zh'
PORT = 2001


#NMT
sys.path.append('../../')
import server_translate

class Server:
    def __init__(self):
        # set up logging
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
        logger = logging.getLogger('NMTSERVER')
        #
        self.logger  = logger
        # initialize list of supported systemIds per pair
        # Load the NMT into memory
        self.models = ['../../8k.model.npz']
        self.source_file = None
        self.saveto = None
        self.k = 3
        self.n_process = 1
        ##
        server_translate.Load_Model(self.models, self.source_file, self.saveto, save_alignment=True, k=self.k,normalize=False, n_process=self.n_process, chr_level=False, verbose=False, nbest=False, suppress_unk=True, a_json=False, print_word_probabilities=False, return_hyp_graph=False)
        self.logger.info('Starting NMT Model!!')
        
    def translate(self, task):
        task['align'] = self.S2B(task['align'])
        result = server_translate.translate(task['text'], self.saveto, save_alignment=task['align'], k=self.k,normalize=False, n_process=self.n_process, chr_level=False, verbose=True, nbest=False, suppress_unk=False, a_json=True, print_word_probabilities=False, return_hyp_graph=False)
        #translation = "Fake OHHH"
        
        return {'text': result['translation'], 'align': [result['align']], 'nbest': [
            {'hyp': result['translation'],
             'align': [],
             'totalScore': 666,
             'word-align': []}]}
    def S2B(self,S):
        if S == "true" or S == "True":
            return True
        else:
            return False


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2?src=' + SRC_LANG + ';tgt=' + TGT_LANG,)


class ThreadedXMLRPCServer(SocketServer.ThreadingMixIn,
                           SimpleXMLRPCServer):
    """Multithreaded SimpleXMLRPCServer"""
    pass


obj = Server()
server = ThreadedXMLRPCServer(("0.0.0.0", PORT), requestHandler=RequestHandler)
server.register_instance(obj)

print "Listening on port " + str(PORT)
server.serve_forever()