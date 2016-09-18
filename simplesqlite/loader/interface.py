# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc
import threading

import dataproperty
import six


@six.add_metaclass(abc.ABCMeta)
class TableLoaderInterface(object):
    """
    Interface class of table loader class.
    """

    @abc.abstractmethod
    def load(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def format_name(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _validate(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _validate_table_name(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _validate_source(self):  # pragma: no cover
        pass


class TableLoader(TableLoaderInterface):
    """
    Abstract class of table data file loader.

    .. py:attribute:: table_name

        Table name string.

    .. py:attribute:: source

        Table data source to load.
    """

    def __init__(self, source):
        self.table_name = "%(default)s"
        self.source = source

        self.__table_count_lock = threading.Lock()
        self.__global_table_count = 0
        self.__format_table_count = {}

    def make_table_name(self):
        self._validate()

        return self.table_name
    def inc_table_count(self):
        with self.__table_count_lock:
            self.__global_table_count += 1
            self.__format_table_count[self.format_name] = (
                self.__format_table_count.get(self.format_name, 0) + 1)

    @abc.abstractmethod
    def _get_default_table_name_template(self):  # pragma: no cover
        pass

    def _validate(self):
        self._validate_table_name()
        self._validate_source()

    def _validate_table_name(self):
        try:
            if dataproperty.is_empty_string(self.table_name):
                raise ValueError("table name is empty")
        except (TypeError, AttributeError):
            raise TypeError("table_name expected to a string")

    def _validate_source(self):
        if dataproperty.is_empty_string(self.source):
            raise ValueError("data source is empty")
