from sx1262 import SX1262
import time
from machine import Pin

pin = Pin("LED", Pin.OUT)

def flash_led(N, delay_ms):
    for n in range (1,N+1):
        pin.toggle()
        time.sleep_ms(delay_ms)
        pin.toggle()
        time.sleep_ms(delay_ms)


def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print('Receive: {}, {}'.format(msg, error))
        flash_led(4, 50)
        
    elif events & SX1262.TX_DONE:
        # Send out signal
        print('TX done.')
        flash_led(2, 100)


sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)



# LoRa
sx.begin(freq=868, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

# FSK
##sx.beginFSK(freq=923, br=48.0, freqDev=50.0, rxBw=156.2, power=-5, currentLimit=60.0,
##            preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
##            addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
##            crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
##            fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
##            tcxoVoltage=1.6, useRegulatorLDO=False,
##            blocking=True)

# Switch callback
def sw_cb():
    print("Pressed!")

# Identify which board this is
print("PING")
pin.on()

# Setup callbacks
sx.setBlockingCallback(False, cb)

#p2.irq(lambda pin: print("IRQ with flags:", pin.irq().flags()), Pin.IRQ_FALLING)

# Main Loop
while True:
    sx.send(b'Ping')
    time.sleep(5)
