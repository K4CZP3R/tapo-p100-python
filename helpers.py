import base64
def mime_encoder(to_encode: bytes):
    encoded_list = list(base64.b64encode(to_encode).decode("UTF-8"))

    count = 0
    for i in range(76, len(encoded_list), 76):
        encoded_list.insert(i + count, '\r\n')
        count += 1
    return ''.join(encoded_list)
