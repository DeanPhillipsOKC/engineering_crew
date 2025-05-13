param(
    [int]$HostPort = 8501,
    [string]$ImageName = "streamlit-app"
)

docker build -t $ImageName .
docker run --rm -p $HostPort`:8501 $ImageName