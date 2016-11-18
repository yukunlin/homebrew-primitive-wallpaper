class Primitive < Formula
    desc "Reproducing images with geometric primitives"
    homepage "https://github.com/fogleman/primitive"
    head "https://github.com/fogleman/primitive.git", :branch => "master"

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
