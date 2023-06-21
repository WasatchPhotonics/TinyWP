
import TinyWP

def process(device):

    # this is based on WasatchPY > FeatureIdentificationDevice.py:1155

    ########################################################################
    # Apply InGaAs even/odd gain/offset in software
    ########################################################################
    # TODO TinyWP read from EEPROM
    eeprom_hardware_even_odd = False
    if TinyWP.is_ingaas(device) and eeprom_hardware_even_odd:
        pass
        # WasatchPY._correct_ingaas_gain_and_offset(spectrum)
        # ditch the breakout when even==odd
        # reimplement in array-based programming
        # dw about the "back out of previous applied"
        # just assume correctness & write equivalent code


    ########################################################################
    # Area Scan (rare)
    ########################################################################

    # consider supporting only fast area scan ?

    # discard everything and return raw pixel data (temporary)
    return TinyWP.get_spectrum(device)

