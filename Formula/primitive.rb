class Primitive < Formula
    desc "Reproducing images with geometric primitives"
    homepage "https://github.com/fogleman/primitive"
    url "https://github.com/fogleman/primitive.git", :revision => "37639cc7a097081d00f46dc0950ec5d8b44c35bd"
    head "https://github.com/fogleman/primitive.git", :branch => "master"
    version "1.0"


    depends_on "go" => :build
    depends_on "imagemagick"

    def install
        ENV["GOPATH"] = buildpath

        # dependencies
        system "go", "get", "github.com/nfnt/resize"
        system "go", "get", "github.com/fogleman/primitive/primitive"

        # build
        system "go", "build", "-o", "/tmp/primitive"

        # install
        bin.install "/tmp/primitive"
    end
end
