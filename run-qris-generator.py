# %%
import re

def convert_crc16(qris_str):
    def char_code_at(s, idx):
        return ord(s[idx])

    crc = 0xFFFF
    strlen = len(qris_str)

    for c in range(strlen):
        crc ^= char_code_at(qris_str, c) << 8
        for i in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    hex_crc = crc & 0xFFFF
    return "{:04X}".format(hex_crc)

def convert_qris_to_dynamic(qris, amount, service_fee=None, is_percent=False):
    qris = qris[:-4]  # Remove the last 4 characters (CRC16)
    
    # Modify static QRIS to dynamic
    qris = qris.replace("010211", "010212", 1)  # Make it dynamic by changing 010211 to 010212
    amount_str = f"54{len(str(amount)):02d}{amount}"  # Format amount
    
    # Split QRIS string
    qris_parts = re.split(r"5802ID", qris)
    
    # Add service fee if present
    if service_fee:
        if is_percent:
            fee_str = f"55020357{len(str(service_fee)):02d}{service_fee}"
        else:
            fee_str = f"55020256{len(str(service_fee)):02d}{service_fee}"
        amount_str += fee_str
    
    # Reconstruct QRIS with amount and service fee
    final_qris = f"{qris_parts[0]}{amount_str}5802ID{qris_parts[1]}"
    
    # Add CRC16 checksum
    crc16_checksum = convert_crc16(final_qris)
    final_qris += crc16_checksum
    
    return final_qris

if __name__ == '__main__':
    # Example usage for toko mpok nas ayam goreng kampung cibubur
    qris_static = "00020101021126620013ID.FINPAY.WWW01189360077732408206950212FM24082006950303UKE51440014ID.CO.QRIS.WWW0215ID10243396247500303UKE5204581253033605802ID5921FIFTYPLUSONE CULINARY6006BEKASI61051743262070703A016304F7AD"

    amount = 50000 # 50rb
    add_service_fee = 'y'

    service_fee = None
    is_percent = False

    if add_service_fee.lower() == 'y':
        fee_type = 'r'
        if fee_type.lower() == 'r':
            service_fee = '0'
        elif fee_type.lower() == 'p':
            service_fee = '0'
            is_percent = True

    # Convert the QRIS string to dynamic with the provided amount and optional service fee
    qris_dynamic = convert_qris_to_dynamic(qris_static, amount, service_fee, is_percent)

    print(f"\n[+] Dynamic QRIS Result: {qris_dynamic}")


