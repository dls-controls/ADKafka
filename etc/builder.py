from iocbuilder import Device, AutoSubstitution, Architecture, SetSimulation
from iocbuilder.arginfo import *
from iocbuilder.modules.asyn import Asyn, AsynPort, AsynIP

from iocbuilder.modules.ADCore import ADCore, ADBaseTemplate, NDFileTemplate, makeTemplateInstance, includesTemplates

# Library names differ between windows and linux.
epics_host_arch = Architecture()
is_windows = epics_host_arch.find('win') >= 0

@includesTemplates(ADBaseTemplate, NDFileTemplate)
class kafkaPluginTemplate(AutoSubstitution):
    TemplateFile = "ADPluginKafka.template"

class KafkaPlugin(AsynPort):
    """This plugin can compress NDArrays to HDF5 and write them to file"""
    # This tells xmlbuilder to use PORT instead of name as the row ID
    UniqueName = "PORT"
    _SpecificTemplate = kafkaPluginTemplate

    def __init__(self, PORT, NDARRAY_PORT, BROKER_ADDR, TOPIC, QUEUE = 3, BLOCK = 1, NDARRAY_ADDR = 0, **args):
        # Init the superclass (AsynPort)
        self.__super.__init__(PORT)
        # Update the attributes of self from the commandline args
        self.__dict__.update(locals())
        # Make an instance of our template
        makeTemplateInstance(self._SpecificTemplate, locals(), args)

    ArgInfo = _SpecificTemplate.ArgInfo + makeArgInfo(__init__,
        PORT = Simple('Port name for the Kafka plugin', str),
        QUEUE = Simple('Input array queue size', int),
        BLOCK = Simple('Blocking callbacks?', int),
        NDARRAY_PORT = Ident('Input array port', AsynPort),
        NDARRAY_ADDR = Simple('Input array port address', int),
        BROKER_ADDR = Simple('Kafka Broker address', str),
        TOPIC = Simple('Kafka topic', str))

    def Initialise(self):
        print '# KafkaPluginConfigure(portName, queueSize, blockingCallbacks, NDArrayPort, NDArrayAddr, maxMemory, brokerAddress, topic)' % self.__dict__
        print 'KafkaPluginConfigure("%(PORT)s", %(QUEUE)d, %(BLOCK)d, "%(NDARRAY_PORT)s", %(NDARRAY_ADDR)s, -1, %(BROKER_ADDR)s, %(TOPIC)s)' % self.__dict__


