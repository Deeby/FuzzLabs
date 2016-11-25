from __primitive import __primitive__

all_properties = [
    {
        "name": "name",
        "type": "str",
        "error": "primitive requires name to be of type str"
    },
    {
        "name": "value",
        "type": "str",
        "mandatory": 1,
        "error": "primitive requires value to be of type str"
    },
    {
        "name": "size",
        "type": ["int", "long"],
        "default": 0,
        "error": "primitive requires size to be of type int or long"
    },
    {
        "name": "max_length",
        "type": ["int", "long"],
        "default": 0,
        "error": "primitive requires max_length to be of type int or long"
    },
    {
        "name": "ascii",
        "type": ["int", "long"],
        "default": 0,
        "error": "primitive requires ascii to be of type int or long"
    },
    {
        "name": "padding",
        "type": "str",
        "default": "\x00",
        "error": "primitive requires padding to be a character"
    },
    {
        "name": "fuzzable",
        "type": "bool",
        "values": [0, 1],
        "default": 1,
        "error": "primitive requires fuzzable to be of type bool (1 or 0)"
    }
]

# =============================================================================
#
# =============================================================================

class string(__primitive__):

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, properties, parent):
        global all_properties
        __primitive__.__init__(self, properties, all_properties, parent)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def init_library(self):
        temp_library = [
            "",

            self.value * 2,
            self.value * 10,
            self.value * 100,
            self.value * 1000,

            self.value * 2 + "\xfe",
            self.value * 10 + "\xfe",
            self.value * 100 + "\xfe",
            self.value * 1000 + "\xfe",

            "/.:/"  + "A"*5000 + "\x00\x00",
            "/.../" + "A"*5000 + "\x00\x00",
            "/.../.../.../.../.../.../.../.../.../.../",
            "/../../../../../../../../../../../../etc/passwd",
            "/../../../../../../../../../../../../boot.ini",
            "..:..:..:..:..:..:..:..:..:..:..:..:..:",
            "\\\\*",
            "\\\\?\\",
            "/\\" * 5000,
            "/." * 5000,
            "!@#$%%^#$%#$@#$%$$@#$%^^**(()",
            "%01%02%03%04%0a%0d%0aADSF",
            "%01%02%03@%04%0a%0d%0aADSF",
            "/%00/",
            "%00/",
            "%00",
            "%u0000",
            "%\xfe\xf0%\x00\xff",
            "%\xfe\xf0%\x01\xff" * 20,

            # format strings.
            "%n"     * 100,
            "%n"     * 500,
            "\"%n\"" * 500,
            "%s"     * 100,
            "%s"     * 500,
            "%100s"  * 500,
            "\"%s\"" * 500,

            # command injection.
            "|touch /tmp/FUZZLABS",
            ";touch /tmp/FUZZLABS;",
            "|notepad",
            ";notepad;",
            "\nnotepad\n",

            # SQL injection.
            "1;SELECT%20*",
            "'sqlattempt1",
            "(sqlattempt2)",
            "OR%201=1",
            "' BENCHMARK(2500000000, MD5(1)) --",
            "\' BENCHMARK(2500000000, MD5(1)) --",
            "\" BENCHMARK(2500000000, MD5(1)) --",
            "' BENCHMARK(2500000000, MD5(1)) /*",
            "\' BENCHMARK(2500000000, MD5(1)) /* ",
            "\" BENCHMARK(2500000000, MD5(1)) /*",
            "' BENCHMARK(2500000000, MD5(1)) #",
            "\' BENCHMARK(2500000000, MD5(1)) #",
            "\" BENCHMARK(2500000000, MD5(1)) #",
            "' BENCHMARK(2500000000, MD5(1)) -- /*",
            "\' BENCHMARK(2500000000, MD5(1)) -- /*",
            "\" BENCHMARK(2500000000, MD5(1)) -- /*",
            "' BENCHMARK(2500000000, MD5(1)) -- #",
            "\' BENCHMARK(2500000000, MD5(1)) -- #",
            "\" BENCHMARK(2500000000, MD5(1)) -- #",
            "' WAITFOR DELAY '01:10:10' --",
            "\' WAITFOR DELAY '01:10:10' --",
            "\" WAITFOR DELAY '01:10:10' --",
            "' WAITFOR DELAY '01:10:10' /*",
            "\' WAITFOR DELAY '01:10:10' /*",
            "\" WAITFOR DELAY '01:10:10' /*",
            "' WAITFOR DELAY '01:10:10' #",
            "\' WAITFOR DELAY '01:10:10' #",
            "\" WAITFOR DELAY '01:10:10' #",
            "' WAITFOR DELAY '01:10:10' -- /*",
            "\' WAITFOR DELAY '01:10:10' -- /*",
            "\" WAITFOR DELAY '01:10:10' -- /*",
            "' WAITFOR DELAY '01:10:10' -- #",
            "\' WAITFOR DELAY '01:10:10' -- #",
            "\" WAITFOR DELAY '01:10:10' -- #",
            "\' BENCHMARK(2500000000, MD5(1)) --",
            "\\' BENCHMARK(2500000000, MD5(1)) --",
            "\" BENCHMARK(2500000000, MD5(1)) --",
            "\' BENCHMARK(2500000000, MD5(1)) /*",
            "\\' BENCHMARK(2500000000, MD5(1)) /* ",
            "\" BENCHMARK(2500000000, MD5(1)) /*",
            "\' BENCHMARK(2500000000, MD5(1)) #",
            "\\' BENCHMARK(2500000000, MD5(1)) #",
            "\" BENCHMARK(2500000000, MD5(1)) #",
            "\' BENCHMARK(2500000000, MD5(1)) -- /*",
            "\\' BENCHMARK(2500000000, MD5(1)) -- /*",
            "\" BENCHMARK(2500000000, MD5(1)) -- /*",
            "\' BENCHMARK(2500000000, MD5(1)) -- #",
            "\\' BENCHMARK(2500000000, MD5(1)) -- #",
            "\" BENCHMARK(2500000000, MD5(1)) -- #",
            "\' WAITFOR DELAY \'01:10:10\' --",
            "\\' WAITFOR DELAY \'01:10:10\' --",
            "\" WAITFOR DELAY \'01:10:10\' --",
            "\' WAITFOR DELAY \'01:10:10\' /*",
            "\\' WAITFOR DELAY \'01:10:10\' /*",
            "\" WAITFOR DELAY \'01:10:10\' /*",
            "\' WAITFOR DELAY \'01:10:10\' #",
            "\\' WAITFOR DELAY \'01:10:10\' #",
            "\" WAITFOR DELAY \'01:10:10\' #",
            "\' WAITFOR DELAY \'01:10:10\' -- /*",
            "\\' WAITFOR DELAY \'01:10:10\' -- /*",
            "\" WAITFOR DELAY \'01:10:10\' -- /*",
            "\' WAITFOR DELAY \'01:10:10\' -- #",
            "\\' WAITFOR DELAY \'01:10:10\' -- #",
            "\" WAITFOR DELAY \'01:10:10\' -- #",
            "\\' BENCHMARK(2500000000, MD5(1)) --",
            "\\\\' BENCHMARK(2500000000, MD5(1)) --",
            "\" BENCHMARK(2500000000, MD5(1)) --",
            "\\\" BENCHMARK(2500000000, MD5(1)) --",
            "\\' BENCHMARK(2500000000, MD5(1)) /*",
            "\\\\' BENCHMARK(2500000000, MD5(1)) /* ",
            "\" BENCHMARK(2500000000, MD5(1)) /*",
            "\\\" BENCHMARK(2500000000, MD5(1)) /*",
            "\\' BENCHMARK(2500000000, MD5(1)) #",
            "\\\\' BENCHMARK(2500000000, MD5(1)) #",
            "\" BENCHMARK(2500000000, MD5(1)) #",
            "\\\" BENCHMARK(2500000000, MD5(1)) #",
            "\\' BENCHMARK(2500000000, MD5(1)) -- /*",
            "\\\\' BENCHMARK(2500000000, MD5(1)) -- /*",
            "\" BENCHMARK(2500000000, MD5(1)) -- /*",
            "\\\" BENCHMARK(2500000000, MD5(1)) -- /*",
            "\\' BENCHMARK(2500000000, MD5(1)) -- #",
            "\\\\' BENCHMARK(2500000000, MD5(1)) -- #",
            "\" BENCHMARK(2500000000, MD5(1)) -- #",
            "\\\" BENCHMARK(2500000000, MD5(1)) -- #",
            "\\' WAITFOR DELAY \\'01:10:10\\' --",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' --",
            "\" WAITFOR DELAY \\'01:10:10\\' --",
            "\\\" WAITFOR DELAY \\'01:10:10\\' --",
            "\\' WAITFOR DELAY \\'01:10:10\\' /*",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' /*",
            "\" WAITFOR DELAY \\'01:10:10\\' /*",
            "\\\" WAITFOR DELAY \\'01:10:10\\' /*",
            "\\' WAITFOR DELAY \\'01:10:10\\' #",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' #",
            "\" WAITFOR DELAY \\'01:10:10\\' #",
            "\\\" WAITFOR DELAY \\'01:10:10\\' #",
            "\\' WAITFOR DELAY \\'01:10:10\\' -- /*",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' -- /*",
            "\" WAITFOR DELAY \\'01:10:10\\' -- /*",
            "\\\" WAITFOR DELAY \\'01:10:10\\' -- /*",
            "\\' WAITFOR DELAY \\'01:10:10\\' -- #",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' -- #",
            "\" WAITFOR DELAY \\'01:10:10\\' -- #",
            "\\\" WAITFOR DELAY \\'01:10:10\\' -- #",
            "\\' BENCHMARK(2500000000, MD5(1)) --",
            "\\\\' BENCHMARK(2500000000, MD5(1)) --",
            "\" BENCHMARK(2500000000, MD5(1)) --",
            "\\\" BENCHMARK(2500000000, MD5(1)) --",
            "\\' BENCHMARK(2500000000, MD5(1)) /*",
            "\\\\' BENCHMARK(2500000000, MD5(1)) /* ",
            "\" BENCHMARK(2500000000, MD5(1)) /*",
            "\\\" BENCHMARK(2500000000, MD5(1)) /*",
            "\\' BENCHMARK(2500000000, MD5(1)) #",
            "\\\\' BENCHMARK(2500000000, MD5(1)) #",
            "\" BENCHMARK(2500000000, MD5(1)) #",
            "\\\" BENCHMARK(2500000000, MD5(1)) #",
            "\\' BENCHMARK(2500000000, MD5(1)) -- /*",
            "\\\\' BENCHMARK(2500000000, MD5(1)) -- /*",
            "\" BENCHMARK(2500000000, MD5(1)) -- /*",
            "\\\" BENCHMARK(2500000000, MD5(1)) -- /*",
            "\\' BENCHMARK(2500000000, MD5(1)) -- #",
            "\\\\' BENCHMARK(2500000000, MD5(1)) -- #",
            "\" BENCHMARK(2500000000, MD5(1)) -- #",
            "\\\" BENCHMARK(2500000000, MD5(1)) -- #",
            "\\' WAITFOR DELAY \\'01:10:10\\' --",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' --",
            "\" WAITFOR DELAY \\'01:10:10\\' --",
            "\\\" WAITFOR DELAY \\'01:10:10\\' --",
            "\\' WAITFOR DELAY \\'01:10:10\\' /*",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' /*",
            "\" WAITFOR DELAY \\'01:10:10\\' /*",
            "\\\" WAITFOR DELAY \\'01:10:10\\' /*",
            "\\' WAITFOR DELAY \\'01:10:10\\' #",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' #",
            "\" WAITFOR DELAY \\'01:10:10\\' #",
            "\\\" WAITFOR DELAY \\'01:10:10\\' #",
            "\\' WAITFOR DELAY \\'01:10:10\\' -- /*",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' -- /*",
            "\" WAITFOR DELAY \\'01:10:10\\' -- /*",
            "\\\" WAITFOR DELAY \\'01:10:10\\' -- /*",
            "\\' WAITFOR DELAY \\'01:10:10\\' -- #",
            "\\\\' WAITFOR DELAY \\'01:10:10\\' -- #",
            "\" WAITFOR DELAY \\'01:10:10\\' -- #",
            "\\\" WAITFOR DELAY \\'01:10:10\\' -- #",
            "; SELECT+pg_sleep(2000) --",
            "); SELECT+pg_sleep(2000) --",
            ")); SELECT+pg_sleep(2000) --",
            "))); SELECT+pg_sleep(2000) --",
            "))); SELECT+pg_sleep(2000) --",
            "'; SELECT+pg_sleep(2000) --",
            "'); SELECT+pg_sleep(2000) --",
            "')); SELECT+pg_sleep(2000) --",
            "'))); SELECT+pg_sleep(2000) --",
            "')))); SELECT+pg_sleep(2000) --",
            "\"; SELECT+pg_sleep(2000) --",
            "\"); SELECT+pg_sleep(2000) --",
            "\")); SELECT+pg_sleep(2000) --",
            "\"))); SELECT+pg_sleep(2000) --",
            "\")))); SELECT+pg_sleep(2000) --",
            "\'; SELECT+pg_sleep(2000) --",
            "\'); SELECT+pg_sleep(2000) --",
            "\')); SELECT+pg_sleep(2000) --",
            "\'))); SELECT+pg_sleep(2000) --",
            "\')))); SELECT+pg_sleep(2000) --",

            # some binary strings.
            "\xde\xad\xbe\xef",
            "\xde\xad\xbe\xef" * 10,
            "\xde\xad\xbe\xef" * 100,
            "\xde\xad\xbe\xef" * 1000,
            "\xde\xad\xbe\xef" * 10000,
            "\x00"             * 1000,

            # miscellaneous.
            "\r\n" * 100,
            "<>" * 500
        ]

        # Add some long strings
        longs = ["A", "B", "1", "2", "3", "<", ">", "'", "\"", "/", "\\", "?",
                 "=", "a=", "&", ".", ",", "(", ")", "]", "[", "%", "*", "-",
                 "('", "')", "(*", "*)",
                 "_", "+", "{", "}", "%s", "%d", "%n", "\x14", "\xFE", "\xFF"]

        for to_long in longs:
            temp_library += self.add_long_strings(to_long)

        # add some long strings with null bytes thrown in the middle of it.
        for length in [128, 256, 1024, 2048, 4096, 10000, 15000, 20000,
                       25000, 32767, 50000, 0xFFFF]:
            s = "B" * length
            s = s[:len(s)/2] + "\x00" + s[len(s)/2:]
            temp_library.append(s)

        for item in temp_library:
            v = item

            if self.ascii:
                if all(i >= 32 for i in map(ord, item)) and all(i <= 126 for i in map(ord, item)):
                    pass
                else:
                    continue

            if self.get('max_length'):
                if len(v) > self.get('max_length'):
                    v = v[:self.get('max_length')]

            if self.get('size'):
                if len(v) > self.get('size'): continue
                v = v + self.get('padding') * (self.get('size') - len(v))

            if v not in self.library: self.library.append(v)

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def add_long_strings(self, sequence):
        '''
        Given a sequence, generate a number of selectively chosen strings 
        lengths of the given sequence and add to the string heuristic library.
        @type  sequence: String
        @param sequence: Sequence to repeat for creation of fuzz strings.
        '''

        l = []
        for length in [128, 255, 256, 257, 511, 512, 513, 1023, 1024, 2048, 
                       2049, 4095, 4096, 4097, 5000, 10000, 15000, 20000,
                       25000, 32762, 32763, 32764, 32765, 32766, 32767, 
                       32768, 32769, 0xFFFF-2, 0xFFFF-1, 0xFFFF, 0xFFFF+1,
                       0xFFFF+2, 99999, 100000, 500000, 1000000]:

            l.append(sequence * length)
        return l

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def render(self):
        value = super(string, self).render()
        return value

