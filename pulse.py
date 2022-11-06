from time import sleep
import pulsectl


class PulseClient(object):

    def __init__(self, client_name, server="tcp:192.168.5.79") -> None:
        pulse = pulsectl.Pulse(client_name=client_name, server=server)
        server_info = pulse.server_info()
        # print(server_info)

        self.__pulse = pulse

    def __new__(cls, *args, **kwargs):
        if not hasattr(PulseClient, "__instance"):
            PulseClient.__instance = object.__new__(cls)
        return PulseClient.__instance

    def getSinkList(self):
        sinks = self.__pulse.sink_list()
        return sinks

    def getSinkByIndex(self, index):
        sinks = self.getSinkList()
        filter_res_addr = filter(lambda i: i.index == index, sinks)
        filter_res = list(filter_res_addr)
        sink = None
        if len(filter_res):
            sink = filter_res[0]
        return sink

    def getSourcesList(self):
        sources = self.__pulse.source_list()
        return sources

    def getSourceByIndex(self, index):
        sources = self.getSourcesList()
        filter_res = list(filter(lambda i: i.index == index, sources))
        source = None
        if (len(filter_res)):
            source = filter_res[0]
        return source

    def setSinkVolume(self, sink_index, volume, du=5000, inter=100, smooth=True,):
        sink = self.getSinkByIndex(sink_index)
        if not sink:
            print("目标设备不存在！")
            return False
        if smooth:
            # 获取当前音量
            current_volume = self.__pulse.volume_get_all_chans(sink)
            volume_offset = volume - current_volume
            ms_step = volume_offset / (du / inter)
            while du:
                self.__pulse.volume_change_all_chans(sink, ms_step)
                du -= inter
                print("当前音量 ", self.__pulse.volume_get_all_chans(sink))
                sleep(inter / 1000)

            self.__pulse.volume_set_all_chans(sink, volume)
        else:
            self.__pulse.volume_set_all_chans(sink, volume)


client = PulseClient("test")


client.setSinkVolume(3, 0., 3000)
