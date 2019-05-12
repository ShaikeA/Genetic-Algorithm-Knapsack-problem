"""
The Gene class
"""


class Gene:
    """
    The Gene class
    """

    def __init__(self, g_id, value, weight, ):
        """
        The instructor
        :param value: value of the gene
        :param weight: weight of the gene
        :param g_id: id of the gene
        """
        self.g_id = g_id
        self.value = value
        self.weight = weight

    def get_vals(self):
        """
        Returns the elements of a gene
        :return:
        """
        return self.g_id, self.value, self.weight
