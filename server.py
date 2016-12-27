import SocketServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from SimpleXMLRPCServer import SimpleXMLRPCServer

SRC_LANG = 'en'
TGT_LANG = 'zh'
PORT = 2001


class Server:
    def translate(self, params):
        print params
        print params['text']
        translation = "fake translation"
        return {'text': 'hello world ', 'align': [{'src-start': 0, 'tgt-start': 0, 'src-end': 0},
                                                  {'src-start': 1, 'tgt-start': 1, 'src-end': 1}], 'nbest': [
            {'hyp': 'hello world ',
             'align': [{'src-start': 0, 'tgt-start': 0, 'src-end': 0}, {'src-start': 1, 'tgt-start': 1, 'src-end': 1}],
             'totalScore': -211.3443603515625,
             'word-align': [{'source-word': 0, 'target-word': 0}, {'source-word': 1, 'target-word': 1}]}]}


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
