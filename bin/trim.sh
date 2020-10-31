# remove beginning and ending spaces, convert multiple spaces into one

sed "s: : :g; s:　: :g; s:[ \t][ \t]*: :g; s:^[ \t]*::g; s:[ \t]*$::g" $*

