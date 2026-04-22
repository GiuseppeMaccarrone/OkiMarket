
class Parser:

    @staticmethod
    def id_parser(res):
        parsed_data = []
        for response in res:
            response['_id'] = str(response['_id'])
            parsed_data.append(response)
        return parsed_data
