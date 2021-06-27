'''
::::::::::::::::: [Aggregator] :::::::::::::::::

    ► Takes responses (or lack of) from the
      binary and decides what changes if any 
      should be triggered 
    ► Sends this response as a _SIGNAL to
      the current strategies generator to 
      handel

     > _SIGNAL Codes  

        - 0 :: Continue as before
        - 1 :: Next generator
        - 2 :: Next mutation
        - 3 :: Increase current mutation lifespan
        - 4 :: Increase current generator lifespan

'''