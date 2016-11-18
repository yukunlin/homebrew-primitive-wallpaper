class PrimitiveWallpaper < Formula
    desc "Abstract wallpapers from Flickr, using primitive"
    homepage "https://github.com/yukunlin/homebrew-primitive-wallpaper"
    head "https://github.com/yukunlin/homebrew-primitive-wallpaper.git", :branch => "master"

    depends_on "primitive"
    depends_on "python" if MacOS.version <= :snow_leopard

    resource "requests" do
        url "https://pypi.python.org/packages/2e/ad/e627446492cc374c284e82381215dcd9a0a87c4f6e90e9789afefe6da0ad/requests-2.11.1.tar.gz"
        sha256 "5acf980358283faba0b897c73959cecf8b841205bb4b2ad3ef545f46eae1a133"
    end

    def install
        ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python2.7/site-packages"

        %w[requests].each do |r|
          resource(r).stage do
            system "python", *Language::Python.setup_install_args(libexec/"vendor")
          end
        end

        # run setup.py
        system "python", *Language::Python.setup_install_args(libexec)

        bin.install Dir[libexec/"bin/*"]
        bin.env_script_all_files(libexec/"bin", :PYTHONPATH => ENV["PYTHONPATH"])
    end
end
