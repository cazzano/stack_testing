using Oxygen

@get "/hello" function()
    return "hello"
end

serve(port=5000)

