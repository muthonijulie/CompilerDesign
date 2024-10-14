function lexicalAnalyzer(sourceCode) {
    const tokenPatterns = [
        //here i am skipping the white space
        { type: "WHITESPACE", regex: /^\s+/, skip: true },

        { type: "ADD Operator", regex: /^\+/ },
    
        { type: "MINUS Operator", regex: /^-/ },
    
        { type: "ASSIGNMENT Operator", regex: /^=/ },
        
        { type: "IF Keyword", regex: /^if\b/ },

        {type : "WHILE  Keyword", regex:/^while\b/},
        
        { type: "ELSE Keyword", regex: /^else\b/ },

        { type: " FOR Keyword", regex: /^for\b/ },
        
        { type: "IDENTIFIER", regex: /^[a-zA-Z_]\w*/ },
        
        { type: "NUMBER", regex: /^\d+/ },
        
        { type: "UNRECOGNIZED", regex: /^./ }
    ];

    while (sourceCode.length > 0) {
        let matched = false;

        for (const { type, regex, skip } of tokenPatterns) {
            const match = sourceCode.match(regex);

            if (match) {
                if (!skip) {
                    console.log(`Token: ${type} (${match[0]})`);
                }

                sourceCode = sourceCode.slice(match[0].length);
                matched = true;
                break;
            }
        }

        if (!matched) {
            console.log(` Unrecognized pattern in '${sourceCode}'`);
            break;
        }
    }
}
