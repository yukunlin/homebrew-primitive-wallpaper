class PrimitiveWallpaper < Formula
    desc "Abstract wallpapers from Flickr, using primitive"
    homepage "https://github.com/yukunlin/homebrew-primitive-wallpaper"
    head "https://github.com/yukunlin/homebrew-primitive-wallpaper.git", :branch => "master"

    option "without-launchd", "Without launch agent to generate wallpapers automatically"

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

    if !build.without? "launchd"
        plist_options :startup => true
        def plist; <<-EOS.undent
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
            <dict>
                <key>Label</key>
                <string>#{plist_name}</string>

                <key>ProgramArguments</key>
                <array>
                    <string>#{opt_bin}/primitive-wallpaper</string>
                    <string>-o</string>
                    <string>~/Pictures/primitive-wallpaper</string>
                    <string>-s</string>
                    <string>4000</string>
                </array>

                <key>ProcessType</key>
                <string>Background</string>

                <key>StartCalendarInterval</key>
                <array>
                    <dict>
                        <key>Hour</key>
                        <integer>12</integer>
                        <key>Minute</key>
                        <integer>0</integer>
                    </dict>
                    <dict>
                        <key>Hour</key>
                        <integer>0</integer>
                        <key>Minute</key>
                        <integer>0</integer>
                    </dict>
                </array>
            </dict>
            </plist>
            EOS
        end
    end
end
